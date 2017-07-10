# About the project
## Project description
### Context
Autism is a neurodevelopmental disorder/difference which impacts sensory processing, communication, social interaction and the ability to adapt to new and unexpected situations. We talk about the autism spectrum (which also contains the previously separately diagnosed Asperger syndrome) because the art and severity each autistic trait presents itself varies widely among the autistic population.

In addition to the medical model of autism, which focuses on the impairments of autistic people, it is useful to also adopt a social model. The social model of disability acknowledges the (in this case neurological) differences of the affected group (in this case autistic people). The problems of those people however are seen as a consequence of the society not being adapted to those differences. This perspective therefor allows us to propose new solutions to help autistic people, not by trying to change or cure them, but by trying to change the environment so that it is more adapted and inclusive.

### Problem
Although it has gained interest over the recent years, the general knowledge of autism in our society is still very limited and based mostly on preconceptions that are either very simplified or plain wrong. This is problematic for two reasons. First of all does it prevent the adaptations of the environment proposed by the social model to take place. If our ideas about the nature of the problem are skewed, implementing the right accommodations becomes nearly impossible. On top of that, the burden of communication is with the autistic person.  (And this is before any adaptations/accommodations can take effect.) This puts autistic people under pressure in a context they are often not even comfortable in by nature. The one of standard (verbal) communication.

### Solution
The most prevalent current solution to this problem currently are so called autism id cards.
They aim to help in situations where communication between those unfamiliar with autism and autistic people fails, as well as to raise awareness in general. They usually list some typical communication difficulties of autistic people, have a place for the name of the cardholder and sometimes for contact data of a person to be contacted in case of emergencies.

The usefulness of those cards is however limited by the fact that the autism spectrum is rather broad, and the explanations on the cards very general. Also, as space is limited, there is not much place for personalization. People who don’t identify to what is on the card will rarely carry it with them.

This project aims to develop a product that solves this problem in form of a crossover between traditional autism ID cards and personalizable infographics. It exists of a web app where autistic people can click and write together one or more personalized infographics and make them available to the people they choose through an automatically generated link. To make at least one infographic available for emergencies, cards similar to the traditional autism ID cards could be printed, containing a qr-code to the users default infographic.

The infographics consist of modules which are mostly optional. Examples of possible modules are: general information, preferred ways of communication and communication difficulties, things I’m (not) good at, what helps me when I’m stressed, medical info, contacts. For each module there are predefined choices as well as a free text option.

Through their modularity and high level of personalization as well as the possibility to create different infographics for different occasions the application area of this product is deliberately kept broad.

### Usecases

The solution can be used in a wide range of situations where communication about autism is relevant. These include disclosure of the diagnosis to peers, any situation where autistic people need to or want to ask for accommodations, as well as situations where the behavior of the autistic person attracts or is expected to attract negative attention, or even medical emergencies. Some specific examples are given below:

Going to a new hairdresser or doctor or taking part in a workshop or course are all situations where it could be beneficial for the professional I'll be working with to know I am autistic. Although they might each need different information or level of detail as to what that actually means to me.

Medical emergency is a stressful situation, in which autistic people may behave unexpectedly and have trouble to communicate effectively. If the doctors don’t know the patient is autistic, they may interpret their behavior completely wrong, resulting in the patient not receiving proper treatment. Besides the use of emergency chat applications, a detailed description of the autistic persons differences and needs can inform the doctors without the need for the autistic person to engage in communication at all.

Going on vacation abroad with autistic kids might cause the need to communicate about autism in different languages. The ability to change the languages of the infographics would make the product very useful for this usecase.

### Stakeholders
There are 3 groups of stakeholders: autistic people, parents of autistic children and medical professionals.

## Project timeline
### Preparation (4 weeks)
#### Needfinding
Through interviews with all stakeholders I would like to find an answer to the following questions:
* What are the situations where autistic people and there allies need to give some explanation about autism and what it means for their specific case/situation/needs?
* Do they use tools to help them with this, have they a written or visual document they refer to?
* If they would use tools, what would they be? What properties are important for a good tool?
* What content need to be covered by the tools? (eg. communication, accommodations, contact persons, …)

#### Story boards
After the interviews the most important use cases will be noted down as storyboards for further use during the project.

#### Related work/inspiration
There are no websites with exactly the same purpose. But there are some that do similar things in a slightly different context
* http://www.autismandhealth.org/ s Personalized accommodations report uses a form wizard with mostly checkbox type questions to generate a pdf report for healthcareproviders of autistic people. The questions used here could be used as a starting point for this project.
* http://about.me is not targetted towards autisitic people. It says to target freelancers, entrepreneurs, and side-hustlers, and allows them to make a simple one page website by going through a form wizard. Whereas the autismandhealth can be a source of inspiration regarding content, about.me has a modern, responsive minimalistic design, that could be a source of inspiration regarding user experience.

#### Result
By the end of the preparation phase I should have gathered enough information on the context the tool will be used in as well as the content it should cover.

### Prototyping (2 weeks)
#### Paper prototypes
Using paper prototypes with autistic people and parents of autistic children, the user experience design of the main functionality of the webapp will be refined.

#### Side note
It is not clear a priori whether paper prototypes are the right tool to use for all autistic people. For some those prototypes might not be detailed or concrete enough to be able to work with them. If this appears to be a general problem, an extra round of more detailed digital prototypes might be necessary.

### Implementation (3 months)
During the implementation phase the actual webapp will be implemented in an iterative way (iteration steps of 2-3 weeks).

The following main areas will be covered:
- composition and display of infographics
- management of infographics
- register, login
- translation

Based on the information gathered during the preparation and prototyping phase the above points will be refined into small and well defined features. Those will be prioritized and validated in each iteration. Feedback will be gathered after each iteration step.

For additional functionality such as registration, login, translation, that was not included in the prototyping phase in the beginning, small prototyping sessions can be held during implementation phase.

accessibility will be a focus point throughout the implementation phase.

### Onboarding (2 weeks)
At this stage I will conduct some final user tests to asses the user experience and onboarding process. It is important that the path for first time users to become power user is smooth, so that they don’t get frustrated along the way. Based on the user tests some final optimizations can be done.
