function update_level() {
    let target = $(".level-indicator");
    let ranks = $(".crafts-list input");

    var sum = 0;
    ranks.each(function() {
        sum += Number($(this).val());
    });

    target.text(sum);
}

function update_children(container, bonus_val) {
    let subtrees = container.siblings("ul").children("li");
    subtrees.children(".craft-container").each(function() {
        let sub_tier = Number($(this).data("tier"));
        let sub_val = Number($(this).find("input").val());
        let sub_bonus = bonus_val + sub_tier * sub_val;
        $(this).find(".bonus").text(sub_bonus);
        update_children($(this), sub_bonus);
    });
}

function update_crafts(element) {
    let new_value = element.val();
    let container = element.parent();
    let tier = Number(container.data("tier"));
    let parent_container = container.parent().parent().siblings(".craft-container");
    let parent_bonus = Number(parent_container.find(".bonus").text());
    let bonus_val = tier * Number(new_value) + parent_bonus;
    container.find(".bonus").text(bonus_val);

    update_children(container, bonus_val);
    update_level();
}

function roll_explode() {
    let start = Math.floor(Math.random() * 20) + 1;

    if (start == 20) {
        return start + roll_explode();
    } else {
        return start;
    }
}

$(document).ready(function() {
    $('.craft-container[data-tier="1"] input').each(function() {
        update_crafts($(this));
    });

    $(".crafts-list input").change(function() {
        update_crafts($(this));
    });

    $(".roll-skill").click(function() {
        let bonus = Number($(this).siblings(".bonus").text());
        let skill_name = $(this).text();

        let roll_result = roll_explode();

        let final_result = roll_result + bonus;

        $(".roll-container").find(".roll-result").text("You rolled " +
            skill_name + " and got: " + final_result + ".");

        if (roll_result == 1) {
            $(".roll-container").find(".level-up").text("You've leveled up!");
        } else {
            $(".roll-container").find(".level-up").text("");
        }

        $(".roll-container").show();
    });
});
