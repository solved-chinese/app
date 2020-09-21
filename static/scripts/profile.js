function checkForm () {
    let form = $("#form")[0];
    let is_legal = false;
    
    for (let index = 2; index < form.elements.length-1; index+=2) {
        if (form.elements[index].value !== form.elements[index+1].value) {
            is_legal = true;
        }
    }

    let pattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    if (!pattern.test($("input[name|='email']")[0].value)) {
        is_legal = false;
        alert("Illegal email address.");
    }

    pattern = /^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$/;
    if (!pattern.test($("input[name|='first_name']")[0].value) || !pattern.test($("input[name|='last_name']")[0].value)) {
        if ($("input[name|='first_name']")[0].value !== "" && $("input[name|='last_name']")[0].value !== "") {
            is_legal = false;
            alert("Illegal names");
        }
    }

    if (is_legal) {
        form.submit();
        $("#success-alert").css("visibility", "visible");
    }

}
