function init() {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "http://127.0.0.1:5000/api/search/");
    xhr.send();
    xhr.onreadystatechange = function () {
        if (this.readyState === 4) {
            if ((this.status == 200) && (this.status < 300)) {
                GenerateTable(JSON.parse(this.responseText))
            }
        }
    }
}

function redirectInit() {
    const urlParams = new URLSearchParams(window.location.search);
    const sid = urlParams.get('sid');
    const searchWord = urlParams.get("sw");
    document.getElementById("resultTitle").innerText = "Search Results for: " + searchWord
    console.log(sid)
    getSearchResults(sid)
}

function getSearchResults(sid) {

    const xhr = new XMLHttpRequest();
    xhr.open("GET", "http://127.0.0.1:5000/api/search_result/" + sid);
    xhr.send();
    xhr.onreadystatechange = function () {
        if (this.readyState === 4) {
            if ((this.status == 200) && (this.status < 300)) {
                GenerateResultTable(JSON.parse(this.responseText))
            }
        }
    }
}

function search() {
    sinput = document.getElementById("search-keyword-input");
    console.log("search for " + sinput.value)
    const xhr = new XMLHttpRequest();
    xhr.open("PUT", "http://127.0.0.1:5000/api/search/");
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.onreadystatechange = function () {
        if (this.readyState === 4) {
            if ((this.status == 200) && (this.status < 300)) {
                redirect2results(JSON.parse(this.responseText)[0], sinput.value)
            }
        }
    }
    var data = {}
    data.search_keyword = sinput.value
    xhr.send(JSON.stringify(data))
}

function redirect2results(resultId, searchWord) {
    window.location.href = 'result.html?sid=' + resultId + "&sw=" + searchWord;
}

function GenerateTable(customers) {
    //Build an array containing Customer records.

    //Create a HTML Table element.
    var table = document.createElement("TABLE");
    table.border = "1";

    //Get the count of columns.
    var columnCount = 3;

    //Add the header row.
    var row = table.insertRow(-1);
    var headerCell = document.createElement("TH");
    headerCell.innerHTML = "search keyword";
    row.appendChild(headerCell);
    var headerCell2 = document.createElement("TH");
    headerCell2.innerHTML = "date";
    row.appendChild(headerCell2);

    var columnNames = ["search_keyword", "search_date"]

    //Add the data rows.
    for (var i = 0; i < customers.length; i++) {
        row = table.insertRow(-1);
        for (var j = 0; j < columnCount; j++) {
            var cell = row.insertCell(-1);
            cell.innerHTML = customers[i][columnNames[j]];
            if (j === 2) {
                cell.innerHTML = "<button onclick=\"redirect2results(" + customers[i]["id"] + ", '" + customers[i]["search_keyword"] + " ' )\" >Sonuclari getir</button>"
            }
        }
    }

    var dvTable = document.getElementById("dvTable");
    dvTable.innerHTML = "";
    dvTable.appendChild(table);
}

function GenerateResultTable(results) {
    var resultList = document.getElementById("resultList")

    var listhtml = "";

    for (var i = 0; i < results.length; i++) {
        listhtml += "<div>" +
            "<h4>" + results[i]["title"] + "</h4>" +
            "<img src=" + results[i]["image"] + "> " +
            "<p> " + results[i]["content"] + " < /p>" +
            "<p> " + results[i]["url"] + " </p> " +
            "</div>"
    }

    resultList.innerHTML = listhtml

}