//groups->list of triple tuple; group->(grpId,grpName,members); members->[member]; member->(memberName,memberID)
var PayeeID;

function loadForm1(){
    const ParentDiv = document.querySelector("#AddEventDiv");
    ParentDiv.innerHTML=`
    <form>
        <label for="amount">Enter the amount:</label>
        <input type="number" id="amount" name="amount"><br>
        <input type="button" value="Next" onclick="storeAmountNLoad()">
    </form>
    `
}

var amount;
function storeAmountNLoad() {
    const ParentDiv = document.querySelector("#AddEventDiv");
    amount = document.querySelector("#amount").value;
    // console.log("The amount entered is: " + amount);
    ParentDiv.innerHTML=`
    <form >
        {% for group in groups %}
        <label for="{{ group[0] }}">{{ group[1] }}</label>
        <input type="radio" id="{{ group[0] }}" name="_"><br>
        {% endfor %}
        <label for="null">Indivisual</label>
        <input type="radio" id="null"name="_"><br>
        <input type="button" value="Next" onclick="storeGrpIDNLoad()">
    </form>
    `
}

var GrpID;
function storeGrpIDNLoad(){
    const ParentDiv = document.querySelector("#AddEventDiv");
    var selected = document.querySelector('input[type="radio"]:checked');
    GrpID = selected.id=="null" ? null:selected.id;
    // console.log("Selected grp: " + GrpID);
    ParentDiv.innerHTML=`
    <form >
        {% for member in groups[2] %}
        <label for="{{ member[0] }}">{{ member[1] }}</label>
        <input type="checkbox" id="{{ member[0] }}"><br>
        {% endfor %}
        <input type="button" value="Submit" onclick="storePayeeIDNLoadNSubmit()">
    </form>
    `
}

var Contributers;
function storePayeeIDNLoadNSubmit(){
    const ParentDiv = document.querySelector("#AddEventDiv");
    var checked = document.querySelectorAll('input[type="checkbox"]:checked');
    if(checked.length==0)alert("Select atleast one Payee");
    else{
        Contributers = Array.from(checked).map(function(option){
            return option.id;
        });
        // console.log("Contributers: "+ Contributers);
        ParentDiv.innerHTML=`
        <button type="button" onclick="loadForm1()">Add Entry</button>
        `
        // console.log("entry recorded")
        alert("Expense Recorded in Database");

        const entry= new FormData();
        entry.append("")

        fetch('/add_expense',{
            method:'POST',
            body: entry
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
    }
}
