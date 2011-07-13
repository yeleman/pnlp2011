function addJavascript(js_path, parentTag) {
    /* Adds a <script /> tag for a given JS path.
       usefull for deferred loading of JS files. */
    var parent = document.getElementsByTagName(parentTag)[0];
    var scr = document.createElement('script');
    scr.setAttribute('type', 'text/javascript');
    scr.setAttribute('src', js_path);
    parent.appendChild(scr);
}

function addJQeventHandlerForLargeTable() {
    /* Add (1) event handler on table element.
       on click, it will find the link inside the row clicked and follow URL */
    $("table").click(function (event) {
        var target = $(event.target);
        if (target.is("td"))
            elem = target.parent()
        else 
            elem = target
        url = elem.find("a").attr('href');
        if (url)
            location.href = url;
    });
}

function addClickClassToTRElements() {
    /* adds the .click class to all TR elements with a link inside.
       this prevent filling-up HTML with useless tags on large tables */
    $("tr").each(function () {
        if ($(this).children("td").children("a").attr('href'))
            $(this).addClass('click');
    });
}

function addMessagesClickEvent() {
    $("ul#messages").click(function(event){$(this).hide("slow"); });
}

function addLogoClickEvent() {
    $("#logo").click(function(event) { location.href = '{% url index %}'; });
}

function addJQEventsForValidationList() {
    $("#not_validated tr").click(function (event) {
        url = $(this).children("td").children("a").attr('href');
        if (url)
            location.href = url;
    });
    $("#not_validated tr").each(function () {
        if ($(this).children("td").children("a").attr('href'))
            $(this).addClass('click');
    });
}

function addJQEventCustomFileInput() {
    $("#excel-form").mouseleave(function(event) {
        value = "Parcourir…";
        if ($(this).val())
            value = $(this).val();
        $("#fakefield").prop('value', value);
    });
}

function addJQEventsSubMenu(base_url, base_url_zero) {
    $("#submenu select.browser").change(function (event) {
        value = $(this).val();
        if (!value)
            return;

        if (value != "-1") {
            url = base_url_zero.replace('0', value);
        } else {
            select_id = $(this).attr('id');
            sid = parseInt(select_id.charAt(select_id.length -1));
            if (sid == 0)
                url = base_url;
            else {
                url = base_url_zero.replace('0', $("#browser_select" + (sid - 1)).val());
            }
        }
        location.href = url;
    });
}

function addJQEventsForValidationChange() {
    $("form#report_form input, form#report_form select").change(function (event) {
        $(this).parent().addClass('changed');
    });
    $("#reset_button").click(function (event) {
        event.preventDefault();
        $("form#report_form input, form#report_form select").parent().removeClass('changed');
        $("form#report_form")[0].reset();
    });
    $("form").submit(function (event) {});
    $("#validate_form").click(function (event) {
        event.preventDefault();
        if (confirm("Êtes vous sûr de vouloir valider le rapport ?\nUne fois validé, il ne sera plus modifiable.")) {
            location.href = '{% url report_do_validation report.receipt %}';
        }
    });
}

function addJQEventPeriodChange(base_url, current_entity) {
    $("#period_select").change(function (event) {
        value = $(this).val();
        url = base_url.replace('ent_code', current_entity).replace('111111', value);
        location.href = url;
    });
}

function addJQEventToggleSources() {
    $("#toggle_sources").click(function (event) {
        $("#sources").toggle("quick");
    });
}

function addJQEventPeriodsChange(base_url, current_entity) {
    $("#period_nav select").change(function (event) {
        speriod = $("#speriod_select").val();
        eperiod = $("#eperiod_select").val();
        url = base_url.replace('ent_code', current_entity).replace('111111', speriod).replace('222222', eperiod);
        location.href = url;
    });
}
