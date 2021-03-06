import logging
from itertools import chain
from operator import attrgetter

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.utils import six
from django.utils.crypto import constant_time_compare, salted_hmac
from django.urls import reverse

from .fields import ChoiceArrayField


logger = logging.getLogger('pages')


class PageManager(models.Manager):
    """Custom filter methods related to the Page model."""

    def active(self):
        """Return only active pages."""
        return self.filter(is_active=True)


class Page(models.Model):
    """
    A Page is a collection of Modules with some extras

    A Page has a title and is linked to the :class:`django.contrib.auth.User`
    who created it through the user field.
    It knows whether it is active, visible, an example.
    It can have a token for sharing through a secret url.

    It can contain any number of any type of modules, and has the ability to
    sort them by their position.

    Module types:

    * :class:`pages.models.GeneralInfoModule`
    * :class:`pages.models.CommunicationModule`
    * :class:`pages.models.DoDontModule`
    * :class:`pages.models.MedicationModule`
    * :class:`pages.models.SensoryModule`
    * :class:`pages.models.ContactModule`
    * :class:`pages.models.FreeTextModule`
    * :class:`pages.models.FreeListModule`
    * :class:`pages.models.FreePictureModule`


    """

    objects = PageManager()

    title = models.CharField(verbose_name=_("Page Title"), max_length=255,
                             default="", blank=True,
                             help_text=_("No inspiration? You can leave this "
                                         "field empty or fill it out later"))
    module_num = models.PositiveIntegerField(default=0, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_("User"),
                             on_delete=models.CASCADE,
                             blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_("Created at"),
                                      default=timezone.now,
                                      blank=True)
    is_active = models.BooleanField(verbose_name=_("Is active"),
                                    default=True,
                                    blank=True,
                                    help_text=_("consider non active views "
                                                "as deleted"))
    is_visible = models.BooleanField(verbose_name=_("Is visible"),
                                     default=False,
                                     blank=True,
                                     help_text=_("visible to other users than "
                                                 "the creating user."))
    token = models.CharField(verbose_name=_("Token"), blank=True, default="",
                             max_length=64)
    token_ts = models.DateTimeField(verbose_name=_("Token created at"),
                                    null=True,
                                    blank=True)
    token_count = models.PositiveIntegerField(verbose_name=_("Token Count"),
                                              default=0, blank=True)
    is_example = models.BooleanField(_("Is example"), default=False,
                                     blank=True)

    def get_all_modules(self, **kwargs):
        """
        Returns a list of querysets, one per Module type.
        Kwargs will be passed to the filter method used to get the querysets.
        """
        return [
            self.generalinfomodule_set.filter(**kwargs),
            self.communicationmodule_set.filter(**kwargs),
            self.dodontmodule_set.filter(**kwargs),
            self.medicationmodule_set.filter(**kwargs),
            self.sensorymodule_set.filter(**kwargs),
            self.contactmodule_set.filter(**kwargs),
            self.freetextmodule_set.filter(**kwargs),
            self.freelistmodule_set.filter(**kwargs),
            self.freepicturemodule_set.filter(**kwargs),
        ]

    @property
    def get_all_modules_sorted(self):
        """
        Returns a list of modules sorted by their position field.
        """
        modules = self.get_all_modules()
        return sorted(
            chain(*modules),
            key=attrgetter('position'))

    def module_deleted(self, position):
        """
        Handles cleanup when a Module is deleted.

        Counts down the pages module number.
        Counts down the position of all the modules
        comming after this module.
        """
        modules = self.get_all_modules(position__gt=position)
        for module_q in modules:
            module_q.select_for_update()
            for module in module_q:
                module.position = module.position - 1
                module.save()
                logger.info("decreased module position of module %s (%s)"
                            "of page %s", module.type, module.id, self.id)
        self.module_num = self.module_num - 1
        logger.info("decreased number of modules for page %s  by one to %s",
                    self.id, self.module_num)
        self.save()

    token_key_salt = "uniqid.pages.models.PageTokenGenerator"

    def make_token(self):
        """
        Returns a token that can be used to view the page until
        a new token is generated.
        """
        self.token_count = self.token_count + 1
        self.token_ts = timezone.now()
        self.token = self._make_token_with_timestamp()
        self.save()
        return self.token

    def check_token(self, token):
        """
        Check that the token allows access to this page.
        """
        if not (self.token and token):
            logger.info("token (%s) or page.token(%s: %s) does not exist.",
                        token, self.id, self.token)
            return False
        if not self.is_visible:
            logger.info("trying to access page token view of private page %s",
                        self.id)
            return False
        if not constant_time_compare(self.token, token):
            logger.info("token (%s) does not equal page.token (%s)",
                        token, self.token)
            return False
        return True

    def _make_token_with_timestamp(self):

        hash = salted_hmac(
            self.token_key_salt,
            self._make_hash_value(),
        ).hexdigest()[::2]
        return hash

    def _make_hash_value(self):
        # Ensure results are consistent across DB backends
        return (
            six.text_type(self.pk) + six.text_type(self.token_count) +
            six.text_type(self.token_ts)
        )

    def get_absolute_url(self):
        """
        only for use in the django-admin.
        """
        return reverse('pages:pagepreview', args=[str(self.id), "admin"])

    def __str__(self):
        return self.title


class Module(models.Model):
    """
    Abstract baseclass modules can inherit from. It has a `ForeignKey`
    relationship to :class:`pages.models:Page` and a position field.
    """
    class Meta:
        abstract = True
        ordering = ['page', 'position']

    page = models.ForeignKey(Page, verbose_name=_("Page"),
                             on_delete=models.CASCADE)
    position = models.IntegerField(verbose_name=_("Position"),
                                   help_text=_("1-based"))

    @property
    def type(self):
        """Returns the class name of an object in its original case."""
        return self.__class__.__name__

    @property
    def delete_url_name(self):
        """the url name including its namespace of this models delete page."""
        return "pages:delete{}".format(self.type.lower())

    @property
    def edit_url_name(self):
        """the url name including its namespace of this models update page."""
        return "pages:update{}".format(self.type.lower())


class GeneralInfoModule(Module):
    """
    Module containing general information about the user.
    such as name, (autism related) identity, picture, ...

    identity field uses IDENTITIES as choices.
    """

    class Meta:
        verbose_name = _("General info module")

    ID_AUTISTIC = "01_autistic"
    ID_HAVE_AUT = "02_have_aut"
    ID_SPECTRUM = "03_spectrum"
    ID_ASD = "04_asd"
    ID_NEURODIV = "05_neurodiv"
    ID_ASP_SYN = "06_asp_syn"
    ID_ASPIE = "07_aspie"
    ID_OTHER = "08_other"

    IDENTITIES = (
        (ID_AUTISTIC, _("I am autistic")),
        (ID_HAVE_AUT, _("I have autism")),
        (ID_SPECTRUM, _("I am on the autism spectrum")),
        (ID_ASD, _("I have an autism spectrum disorder")),
        (ID_NEURODIV, _("I am neurodivergent")),
        (ID_ASP_SYN, _("I have Asperger syndrome")),
        (ID_ASPIE, _("I am an aspie")),
        (ID_OTHER, _("Other"))
    )

    template = "pages/_generalinfo.html"

    help_text = _("With this module you can introduce yourself. "
                  "Add a picture if you want to, state your pronouns or "
                  "disclose your autism. As in all our modules, all of this "
                  "is optional.")

    name = models.CharField(verbose_name=_("Name"), max_length=255, default="",
                            blank=True)
    identity = models.CharField(verbose_name=_("Identity"),
                                max_length=32,
                                choices=IDENTITIES,
                                default="",
                                blank=True)
    identity_free = models.CharField(
        verbose_name=_("Specify your identity if you chose other above"),
        max_length=255, default="", blank=True)
    pronouns = models.CharField(verbose_name=_("Prefered pronouns"),
                                max_length=255, default="",
                                blank=True,
                                help_text=_("She/Her/Hers, He/Him/His, "
                                            "They/Them/Theirs, etc."))
    picture = models.ImageField(verbose_name=_("Image"), blank=True,
                                null=True, upload_to="infomodule")
    remarks = models.TextField(verbose_name=_("Remarks"),
                               default="", blank=True)

    def __str__(self):
        return "{page} Generalinfomodule: {name}, {id}"\
            .format(page=str(self.page), name=self.name, id=self.identity)


class CommunicationModule(Module):
    """
    This module contains communication suggestions, and can contain multiple
    :class:`pages.models.CommunicationMethods`.

    The suggestions_choices field uses SUGGESTIONS as choices.
    """

    class Meta:
        verbose_name = _("Communication module")

    template = "pages/_communication.html"

    title = _("Communication")

    help_text = _("This module lets you describe your communication "
                  "preferences in different situations. "
                  "In addition you can give others tips on how to communicate "
                  "effectively with you.")

    SIMPLE = "01_simple"
    CONCRETE = "02_concrete"
    PICTURES = "03_pictures"
    WRITE = "04_write"
    DETAILED = "05_detailed"
    IMPORTANT = "06_important"
    QUESTIONS = "07_questions"
    PROCESSING = "08_processing"
    NOISES = "09_noises"
    NOT_RUDE = "10_not_rude"
    LITERALLY = "11_literally"
    BODY_LANGUAGE = "12_body_language"
    HARD_FLUENT = "13_hard_fluent"
    INVOLVED = "14_involved"
    SITUATION = "15_situation"
    TELEPHONE = "16_telephone"

    SUGGESTIONS = (
        (SIMPLE, _("Use simple words and short sentences.")),
        (CONCRETE, _("Be very concrete and specific. "
                     "Avoid very broad questions.")),
        (PICTURES, _("Show me diagrams or pictures whenever possible.")),
        (WRITE, _("Write down important information or instructions for me.")),
        (DETAILED, _("Give me very detailed information.")),
        (IMPORTANT, _("Focus only on the most important information.")),
        (QUESTIONS, _("Be patient with me if I need to ask a lot of "
                      "questions.")),
        (PROCESSING, _("Give me extra time to process what you have said. "
                       "Especially if I have to answer questions.")),
        (NOISES, _("Do not try to talk to me while there are other noises.")),
        (NOT_RUDE, _("If I seem rude, I don't mean it. "
                     "I'm just really direct.")),
        (LITERALLY, _("I often take language too literally.")),
        (BODY_LANGUAGE, _("I may have difficulty understanding tone of voice, "
                          "facial expressions, or body language.")),
        (HARD_FLUENT, _("I may have a hard time communicating, "
                        "even if my speech sounds fluent.")),
        (INVOLVED, _("I can be involved in decisions "
                     "even though I have difficulty speaking.")),
        (SITUATION, _("My ability to communicate changes a lot, "
                      "depending on the situation.")),
        (TELEPHONE, _("I have a hard time using the telephone."))
    )

    suggestions_choices = ChoiceArrayField(
        models.CharField(max_length=32, choices=SUGGESTIONS),
        verbose_name=_("Communication suggestions"), default=list, blank=True)
    suggestions_free = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("Other communication suggestions"),
        blank=True, default=list)


class CommunicationMethods(models.Model):
    """
    CommunicationMethods belong to a :class:`pages.models.CommunicationModule`.
    They describe prefered communication methods in two directions
    ('me to you' and 'you to me') for a certain situation.

    The fields you_to_me_choices and  me_to_you_choices
    both use METHODS as choices.
    """

    SPOKEN = "01_spoken"
    WRITTEN = "02_written"
    TEXT_AAC = "03_text_aac"
    PIC_AAC = "04_pic_aac"
    OFF_SIGN = "05_off_sign"
    OTHER_SIGN = "06_other_sign"

    METHODS = (
        (SPOKEN, _("Spoken language")),
        (WRITTEN, _("Written language")),
        (TEXT_AAC, _("Text based alternative to speech")),
        (PIC_AAC, _("Picture based alternative to speech")),
        (OFF_SIGN, _("Official sign-language")),
        (OTHER_SIGN, _("Other signs, gestures or behaviours"))
    )

    situation = models.CharField(verbose_name=_("Situation"),
                                 max_length=255, default="", blank=True)
    you_to_me_choices = ChoiceArrayField(
        models.CharField(max_length=32, choices=METHODS),
        verbose_name=_("You can use"), blank=True, default=list)
    you_to_me_free = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("Other communication methods you can use"),
        blank=True, default=list)
    me_to_you_choices = ChoiceArrayField(
        models.CharField(max_length=32, choices=METHODS),
        verbose_name=_("I will use"), blank=True, default=list)
    me_to_you_free = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("Other communication methods I might use"),
        blank=True, default=list)
    module = models.ForeignKey(CommunicationModule, verbose_name=_("module"),
                               on_delete=models.CASCADE)


class DoDontModule(Module):
    """
    Module containing lists of things to 'do', 'ask first' and 'don't do'.

    do_choices field uses DOS as choices.

    ask_choices field uses ASKS as choices.

    dont_choices field uses DONTS as choices.
    """
    class Meta:
        verbose_name = _("Do's and Don'ts module")

    template = "pages/_dodont.html"

    title = _("Do's and Don'ts")

    help_text = _("With this module, you can provide 3 quick lists "
                  "with things people can do, shouldn't do, or should "
                  "ask you first.")

    DO_TIME = "01_do_time"
    DO_LIGHT = "02_do_light"
    DO_QUIET = "03_do_quiet"
    DO_HEADPHONES = "04_do_headphones"
    DO_EAR_PROTECT = "05_do_ear_protect"
    DO_FIDGET = "06_do_fidget"
    DO_CALM = "07_do_calm"
    DO_CHANGES = "08_do_changes"
    DO_NOISES = "09_do_noises"
    DO_INSTRUCTIONS = "10_do_instructions"
    DO_PREPARE = "11_do_prepare"

    ASK_TOUCH = "01_ask_touch"
    ASK_STUFF = "02_ask_stuff"
    ASK_READY = "03_ask_ready"
    ASK_COMMUNICATE = "04_ask_communicate"
    ASK_TALK = "05_ask_talk"

    DONT_TOUCH = "01_dont_touch"
    DONT_EYE = "02_dont_eye"
    DONT_QUESTIONS = "03_dont_questions"
    DONT_CLOSE = "04_dont_close"
    DONT_CHITCHAT = "05_chitchat"
    DONT_TALK = "06_dont_talk"
    DONT_NOISES = "07_dont_noises"

    DOS = (
        (DO_TIME, _("Leave me enough time to answer your questions "
                    "or to make decisions")),
        (DO_LIGHT, _("Use natural light and turn off fluorescent lights "
                     "if possible")),
        (DO_QUIET, _("Try to find a quiet room or space for me")),
        (DO_HEADPHONES, _("Let me use my headphones "
                          "to listen to my favorite music")),
        (DO_EAR_PROTECT, _("Let me use my ear protection "
                           "to block out noises")),
        (DO_FIDGET, _("Let me fidget, move around, flap my arms or "
                      "make other sounds or motions")),
        (DO_CALM, _("Talk to me with a calm voice")),
        (DO_CHANGES, _("Tel me about changes in plans as soon as possible")),
        (DO_NOISES, _("Turn of the TV, radio or other things "
                      "that make noise")),
        (DO_INSTRUCTIONS, _("Give me clear instructions "
                            "if I have to do something")),
        (DO_PREPARE, _("Tell me what is going to happen beforehand"))
    )

    ASKS = (
        (ASK_TOUCH, _("Ask before you touch me")),
        (ASK_STUFF, _("Ask before touching my stuff")),
        (ASK_READY, _("Ask me if I am ready to go (and where we go to) "
                      "before you take me to a new place")),
        (ASK_COMMUNICATE, _("Ask me about what method of communication "
                            "I want to use")),
        (ASK_TALK, _("Ask me if I want to talk or socialize "
                     "before introducing me to new people"))
    )

    DONTS = (
        (DONT_TOUCH, _("Don't touch me without permission")),
        (DONT_EYE, _("Don't force me to make eye contact")),
        (DONT_QUESTIONS, _("Don't ask me too many questions")),
        (DONT_CLOSE, _("Do not sit or stand close to me "
                       "unless it is necessary")),
        (DONT_CHITCHAT, _("Avoid chitchat")),
        (DONT_TALK, _("Don't talk a lot to try to calm me, "
                      "as this has the contrary effect")),
        (DONT_NOISES, _("Don't make unexpected hard noises "
                        "such as slamming a door")),
    )

    do_choices = ChoiceArrayField(
        models.CharField(max_length=32, choices=DOS),
        verbose_name=_("Things others can do to help you"), blank=True,
        default=list)
    do_free = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("More things others can do"),
        blank=True, default=list)
    ask_choices = ChoiceArrayField(
        models.CharField(max_length=32, choices=ASKS),
        verbose_name=_("Things people should ask you about"), blank=True,
        default=list)
    ask_free = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("More things others should ask"),
        blank=True, default=list)
    dont_choices = ChoiceArrayField(
        models.CharField(max_length=32, choices=DONTS),
        verbose_name=_("Things others should not do"), blank=True,
        default=list)
    dont_free = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("More things others shouldn't do"),
        blank=True, default=list)


class MedicationModule(Module):
    """
    This module can contain multiple :class:`pages.models.MedicationItem`.
    """
    class Meta:
        verbose_name = _("Medication module")

    template = "pages/_medication.html"

    title = _("Medication")

    help_text = _("Here you can create a table with your medication and when "
                  "you take how much of it. This can be useful for doctors or "
                  "caregivers, or just as a reminder for yourself.")

    @property
    def edit_url_name(self):
        return "pages:medicationmoduledetail"


class MedicationItem(models.Model):
    """
    MedicationItems belong to a :class:`pages.models.MedicationModule`.

    Each MedicationItem has a name, and a field for remarks

    They can contain multiple :class:`pages.models.MedicationIntake`,
    with further information.

    They have a fixed position within the
    :class:`pages.models.MedicationModule`,
    depending on the order they were added. This position is
    determined by the position field which is set automatically
    in the save method.
    """
    class Meta:
        ordering = ['module', 'position']

    name = models.CharField(verbose_name=_("Medication name"),
                            max_length=255, default="", blank=True)
    remarks = models.TextField(verbose_name=_("Remarks"), default="",
                               blank=True)
    module = models.ForeignKey(MedicationModule, verbose_name=_("module"),
                               on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0, blank=True,
                                           db_index=True)

    def save(self, *args, **kwargs):
        """
        If creating

        sets position field to the current maximum of positions within the
        :class:`pages.models:MedicationModule` +1 and saves the object.

        Else just save the object
        """
        needs_position = self._state.adding
        if needs_position:
            try:
                current_max = self.module.medicationitem_set.all().aggregate(
                    models.Max('position'))['position__max'] or 0

                self.position = current_max + 1
            except (TypeError, IndexError):
                pass
        super().save(*args, **kwargs)


class MedicationIntake(models.Model):
    """
    MedicationIntakes belong to a :class:`pages.models.MedicationItem`.

    Each MedicationIntake has a time and quantity

    They have a fixed position within the :class:`pages.models.MedicationItem`,
    depending on the order they were added. This position is
    determined by the position field which is set automatically
    in the save method.
    """
    class Meta:
        ordering = ['medication', 'position']

    time = models.CharField(verbose_name=_("Intake time"),
                            max_length=255, default="", blank=True)
    quantity = models.CharField(verbose_name=_("Intake quantity"),
                                max_length=255, default="", blank=True)
    medication = models.ForeignKey(MedicationItem,
                                   verbose_name=_("medication"),
                                   on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0, blank=True,
                                           db_index=True)

    def save(self, *args, **kwargs):
        """
        If creating

        sets position field to the current maximum of positions within the
        :class:`pages.models.MedicationItem` +1 and saves the object.

        Else just save the object
        """
        needs_position = self._state.adding
        if needs_position:
            try:
                current_max = self.medication.medicationintake_set.all().\
                    aggregate(models.Max('position'))['position__max'] or 0

                self.position = current_max + 1
            except (TypeError, IndexError):
                pass
        super().save(*args, **kwargs)


class SensoryModule(Module):
    """
    Module containing sensory information.
    One can state how sensitive one is to sound, light, smell and temperature.
    On top of that further sensory information can be added.

    sound, light, smell and temperature fields use RANGE as choices.
    extra_choices uses EXTRAS as choices
    """
    class Meta:
        verbose_name = _("Sensory module")

    template = "pages/_sensory.html"

    title = _("Sensory sensitivities")

    help_text = _("This module presents your sensory profile. You can also "
                  "add other information related to sensory processing.")

    SENS_NONE = "00_sens_none"
    SENS_V_LOW = "01_sens_v_low"
    SENS_LOW = "02_sens_low"
    SENS_MED = "03_sens_med"
    SENS_HIGH = "04_sens_high"
    SENS_V_HIGH = "05_sens_v_high"

    RANGE = (
        (SENS_NONE, _("Do not include")),
        (SENS_V_LOW, _("Very low")),
        (SENS_LOW, _("Lower than average")),
        (SENS_MED, _("Average")),
        (SENS_HIGH, _("Higher than average")),
        (SENS_V_HIGH, _("Very high"))
    )

    EXTRA_FLUO = "01_extra_fluo"
    EXTRA_MULTI = "02_extra_multi"
    EXTRA_PAIN = "03_extra_pain"

    EXTRAS = (
        (EXTRA_FLUO, _("I can't cope with fluorescent lighting")),
        (EXTRA_MULTI, _("I have trouble processing more than on sense at a "
                        "time, for example hearing you while looking at "
                        "something")),
        (EXTRA_PAIN, _("I have difficulties recognizing and or reporting pain "
                       "or other symptoms"))
    )

    sound = models.CharField(verbose_name=_("Sensitivity to sound"),
                             max_length=32,
                             choices=RANGE,
                             default=SENS_NONE)
    light = models.CharField(verbose_name=_("Sensitivity to light"),
                             max_length=32,
                             choices=RANGE,
                             default=SENS_NONE)
    smell = models.CharField(verbose_name=_("Sensitivity to smells"),
                             max_length=32,
                             choices=RANGE,
                             default=SENS_NONE)
    temperature = models.CharField(
        verbose_name=_("Sensitivity to temperature"),
        max_length=32,
        choices=RANGE,
        default=SENS_NONE)
    extra_choices = ChoiceArrayField(
        models.CharField(max_length=32, choices=EXTRAS),
        verbose_name=_("Additional sensory info"), blank=True, default=list)
    extra_free = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("More additional sensory info"),
        blank=True, default=list)

    @property
    def has_sensory_profile(self):
        """
        Does the module have either of the following fields set:
        sound, light, smell, temperature.
        """
        return self.sound != self.SENS_NONE \
            or self.light != self.SENS_NONE \
            or self.smell != self.SENS_NONE \
            or self.temperature != self.SENS_NONE


class ContactModule(Module):
    """
    This module can contain multiple :class:`pages.models.ModuleContact`.
    """
    class Meta:
        verbose_name = _("Contact module")

    template = "pages/_contact.html"

    title = _("Contacts")

    help_text = _("In this module you can add all kinds of contact data. "
                  "As always, all fields are optional, so you can add "
                  "contacts with only a phone number or email address, as "
                  "well as postal addresses and even maps(not available yet).")


class ModuleContact(models.Model):
    """
    ModuleContacts belong to a :class:`pages.models.ContactModule`.
    They have a title, name, address, phone, email, and extra field.
    """
    title = models.CharField(verbose_name=_("Contact title"),
                             max_length=255, default="", blank=True,
                             help_text=_("Choose a descriptive title for the "
                                         "contact. A good title may include "
                                         "the role of this contact, "
                                         "or the situation in which they "
                                         "can be contacted."))
    name = models.CharField(verbose_name=_("Name"),
                            max_length=255, default="", blank=True)
    address = models.TextField(verbose_name=_("Address"), default="",
                               blank=True)
    phone = models.CharField(verbose_name=_("Phone number"),
                             max_length=255, default="", blank=True)
    email = models.EmailField(verbose_name=_("Email address"), default="",
                              blank=True)
    extra = models.TextField(verbose_name=_("Extra comment"), default="",
                             blank=True)
    module = models.ForeignKey(ContactModule, verbose_name=_("module"),
                               on_delete=models.CASCADE)


class FreeTextModule(Module):
    """
    Module for saving free text with a title.
    """
    class Meta:
        verbose_name = _("Free text module")

    help_text = _("Here you can create a custom module containing "
                  "text and a title. You can use it  for any text you want "
                  "to add that doesn't have place in our pre-formulated "
                  "modules.")

    template = "pages/_freetext.html"

    title = models.CharField(verbose_name=_("Title"),
                             max_length=255, default="", blank=True)
    text = models.TextField(verbose_name=_("Text"), default="", blank=True)

    def __str__(self):
        return "{page} Freetextmodule: {title}"\
            .format(page=str(self.page), title=self.title)


class FreeListModule(Module):
    """
    Module for saving a list of items with a title.
    """
    class Meta:
        verbose_name = _("Free list module")

    template = "pages/_freelist.html"

    help_text = _("A place to add your own lists. List things you are good "
                  "at, your hobbies, questions you have prepared for a "
                  "conversation, or anything else you want to make a list of.")

    title = models.CharField(verbose_name=_("Title"),
                             max_length=255, default="", blank=True)
    items = ArrayField(models.CharField(max_length=255),
                       verbose_name=_("Items"), blank=True, default=list)

    def __str__(self):
        return "{page} Freelistmodule: {title}"\
            .format(page=str(self.page), title=self.title)


class FreePictureModule(Module):
    """
    This module has a title field and can contain multiple
    :class:`pages.models.ModulePicture`.
    """
    class Meta:
        verbose_name = _("Free picture module")

    help_text = _("Upload your own pictures and add a title and a description "
                  "to them. Sometimes adding an illustration, cartoon or "
                  "photo helps to bring your message accross.")

    template = "pages/_freepicture.html"

    title = models.CharField(verbose_name=_("Title"),
                             max_length=255, default="", blank=True)

    def __str__(self):
        return "{page} Freelistmodule: {title}"\
            .format(page=str(self.page), title=self.title)


class ModulePicture(models.Model):
    """
    ModulePictures belong to a :class:`pages.models.PictureModule`.
    They have a title, description and picture.
    """
    module = models.ForeignKey(FreePictureModule, verbose_name=_("module"),
                               on_delete=models.CASCADE)
    picture = models.ImageField(verbose_name=_("Image"), blank=True,
                                null=True, upload_to="picturemodule")
    description = models.TextField(verbose_name=_("Image description"),
                                   default="", blank=True)
    title = models.CharField(verbose_name=_("Image title"),
                             max_length=255, default="", blank=True)


MODULES = (
    ("generalinfomodule", GeneralInfoModule._meta.verbose_name),
    ("communicationmodule", CommunicationModule._meta.verbose_name),
    ("dodontmodule", DoDontModule._meta.verbose_name),
    ("medicationmodule", MedicationModule._meta.verbose_name),
    ("sensorymodule", SensoryModule._meta.verbose_name),
    ("contactmodule", ContactModule._meta.verbose_name),
    ("freetextmodule", FreeTextModule._meta.verbose_name),
    ("freelistmodule", FreeListModule._meta.verbose_name),
    ("freepicturemodule", FreePictureModule._meta.verbose_name)
)


MODULE_HELP = {
    "generalinfomodule": GeneralInfoModule.help_text,
    "communicationmodule": CommunicationModule.help_text,
    "dodontmodule": DoDontModule.help_text,
    "medicationmodule": MedicationModule.help_text,
    "sensorymodule": SensoryModule.help_text,
    "contactmodule": ContactModule.help_text,
    "freetextmodule": FreeTextModule.help_text,
    "freelistmodule": FreeListModule.help_text,
    "freepicturemodule": FreePictureModule.help_text
}
