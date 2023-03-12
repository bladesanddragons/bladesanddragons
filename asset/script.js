var combat = document.getElementById("combat-expertise-selected");
if (data["Combat Expertise"]) {
  combat = document.getElementById("combat-expertise-choice");
}
combat.classList.add("hide");

for (key in data) {
  var a = document.getElementById("abilities");
  var e = document.getElementById(key);
  if (e) {
    if (e.classList.contains("value")) {
      e.textContent = data[key];
    } else if (e.classList.contains("skill")) {
      e.classList.add("underline");
    } else if (e.classList.contains("icon")) {
      e.src = e.src.replace(".svg", "-fill.svg");
    }
  } else if (key.startsWith("Options ") || key.startsWith("Description ")) {
    var e = document.createElement("p");
    if (key.startsWith("Options")) {
      e.classList.add("options");
    }
    e.textContent = data[key];
    a.appendChild(e);
  } else {
    var e = document.createElement("p");
    e.classList.add("ability");

    var i = document.createElement("img");
    var shape = "circle";
    if (key.includes("Adept")) {
      shape = "diamond";
    } else if (key.includes("Resilient")) {
      shape = "shield";
    }
    var fill = "-fill";
    if (key.startsWith("Option ")) {
      fill = "";
    }
    i.src = "asset/icon/" + shape + fill + ".svg";
    i.classList.add("icon")
    e.appendChild(i);

    e.appendChild(document.createTextNode(" "));
    var s = document.createElement("strong");
    s.textContent = key.replace("Option ", "");
    e.appendChild(s);
    if (typeof data[key] == "string") {
      e.appendChild(document.createTextNode(" "));
      var t = document.createElement("span");
      t.textContent = data[key];
      e.appendChild(t);
    }
    a.appendChild(e);
  }

}

