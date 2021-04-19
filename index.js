// Get match info:
const status = document.querySelector("#match-detail__status").textContent
const home = document.querySelector("#match-detail__team-name__home").textContent
const away = document.querySelector("#match-detail__team-name__away").textContent
const homeScore = document.querySelector("#match-detail__home__score").textContent
const awayScore = document.querySelector("#match-detail__away__score").textContent

let i = 7;
let j = 7;

const match = {
    idMatch: "m" + i,
    home: home,
    away: away,
    status: status,
    homeScore: homeScore,
    awayScore: awayScore,
    details: "dt" + j
}

console.log(JSON.stringify(match));

//Get raw match details
let eventList = []
document.querySelectorAll(".Details_matchRowWrapper__238ut").forEach(detail => {
    let e = {
        type: "",
        assist: null,
        team: "",
        time: "",
        player: ""
    }
    // Set time for event:
    e.time = detail.firstChild.textContent
    // Left child
    let left = detail.childNodes[1]
    leftLen = left.childNodes.length
    if (left.firstChild.textContent !== "") {
        e.player = left.firstChild.textContent;
        e.team = "home"
        if (leftLen === 2) {
            e.assist = left.lastChild.textContent
            e.type = "goal";
        }
    }

    let right = detail.lastChild;
    rightLen = right.childNodes.length;
    if (right.firstChild.textContent !== "") {
        e.player = right.firstChild.textContent;
        e.team = "away"
        if (rightLen === 2) {
            e.assist = right.lastChild.textContent
            e.type = "goal";
        }
    }

    eventList.push(e)
})

console.log(JSON.stringify(eventList));