function add_formset(element){
  var total_forms_input = $("#"+element.id+"-TOTAL_FORMS");
  var current_num = Number(total_forms_input.val());
  var current_index = current_num - 1;
  var next_num = current_num + 1;
  var fieldset = $("fieldset#"+element.id+"-"+current_index.toString());
  var new_fieldset = fieldset.clone(true);
  // update all the id's
  new_fieldset.find("[id*=-"+current_index.toString()+"], [name*=-"+current_index.toString()+"], [for*=-"+current_index.toString()+"]").add(new_fieldset).each(function(){
    replace_number(this, 'id', current_index, current_num)
    replace_number(this, "name", current_index, current_num)
    replace_number(this, "for", current_index, current_num)
  });
  new_fieldset.find("legend").text(function () {
    return $(this).text().replace(current_num.toString(), next_num.toString());
  });
  // reset all the inputs
  new_fieldset.find(':input').each(function() {
    $(this).val(this.defaultValue);
    if ($(this).prop('type') == "checkbox" || $(this).prop('type') == "radio"){
      $(this).prop( "checked", false );
    };
  });
  new_fieldset.insertAfter(fieldset);
  // updat total forms value
  total_forms_input.val(current_num + 1);
}

function replace_number(element, attr, old_num, new_num){
  var old_attr = $(element).attr(attr);
  if(old_attr){
    var new_attr = old_attr.replace(old_num.toString(), new_num.toString());
    $(element).attr(attr, new_attr);
  }
}
