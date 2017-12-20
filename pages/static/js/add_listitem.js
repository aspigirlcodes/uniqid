function add_item(element){
var parent = $(element).closest("li.input-list-item");
var input_list = $(element).closest("ul.input-list");
var input_element = input_list.find("input.form-control").last()
var last_id = input_element.attr('id');
var components = last_id.split("_");
var prefix = components.shift();
var count = Number(components.pop()) + 1;
var name = components.join("_");
parent.find("span.input-group-btn").remove()
input_list.append($("<li>").addClass("input-list-item")
                  .append($("<div>").addClass("input-group")
                          .append($("<input type='text'>").attr("name", name + "_" + count.toString())
                                                          .addClass("form-control")
                                                          .attr("id", prefix + "_" + name + "_" + count.toString())
                                                          .attr("aria-label", gettext("Item number") + " " + (count + 1).toString())
                                  )
                          .append($("<span>").addClass("input-group-btn")
                                  .append($("<button>").addClass("btn btn-secondary")
                                                       .attr("type", "button")
                                                       .attr("onclick", "add_item(this)")
                                                       .attr("aria-label", gettext("add item"))
                                                       .append("+")
                                         )
                                  )
                          )
                  );
input_list.find("input.form-control").last().focus();
}
