function setUpInfoIcons() {
    var info_icons = document.getElementsByClassName("formula-info-icon");
    for (var i = 0; i < info_icons.length; i++) {
       info_icon = info_icons.item(i);
       info_icon.onclick = showHelpForFormula;
    }
}

function showHelpForFormula() {
    var win = window.open("plotting", "How to use plotting", "toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=550,height=800,top="+(screen.height/3)+",left="+(screen.width));
}
