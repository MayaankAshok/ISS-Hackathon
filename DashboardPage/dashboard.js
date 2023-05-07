//groups->list of triple tuple; group->(grpId,grpName,members); members->[member]; member->(memberName,memberID)
var PayeeID;

function loadForm1(){
    const ParentDiv = document.querySelector("#AddEventDiv")
    ParentDiv.innerHTML=`
    <form>
        <label for="name">Enter Expense Name:</label>
        <input type="text" id="expName" name="amount" required><br>
        <input type="button" value="Next" onclick="storeNameNLoad()">
    </form>
    `    
}

var ExpName;
function storeNameNLoad(){
    ExpName = document.querySelector("#AddEventDiv #expName").value;
    // console.log("Name of Expense: "+ExpName);
    const ParentDiv = document.querySelector("#AddEventDiv");
    ParentDiv.innerHTML=`
    <form>
        <label for="amount">Enter the amount:</label>
        <input type="number" id="amount" name="amount" required><br>
        <input type="button" value="Next" onclick="storeAmountNLoad()">
    </form>
    `
}

var amount;
function storeAmountNLoad() {
    const ParentDiv = document.querySelector("#AddEventDiv");
    amount = document.querySelector("#AddEventDiv #amount").value;

    console.log("The amount entered is: " + amount);
    ParentDiv.innerHTML = "<form >"
    for(var i= 0; i< groups.length; i++){
        ParentDiv.innerHTML += '<label for="'+ groups[i][0] +'">'+ groups[i][1] +'</label>'+
        '<input type="radio" id="'+ groups[i][0]+'" name="_"><br></br>'
    }
    ParentDiv.innerHTML += '<input type="button" value="Next" onclick="storeGrpIDNLoad()"></form>'
}

var GrpID;
function storeGrpIDNLoad(){
    const ParentDiv = document.querySelector("#AddEventDiv");
    var selected = document.querySelector('#AddEventDiv input[type="radio"]:checked');
    if(selected.length==0) alert("Select atleast one group");
    else{
        GrpID = parseInt(selected.id) -1;
        console.log("Selected grp: " + GrpID);
        ParentDiv.innerHTML=`
        <form>`
        for (var i = 0; i< groups[GrpID][2].length; i++){
            var member = groups[GrpID][2][i]
            ParentDiv.innerHTML += '<label for="'+ member[0]+'">'+ member[1] +'</label>'+
            '<input type="checkbox" id="'+ member[0] +'"><br>'
        }
        ParentDiv.innerHTML+= '<input type="button" value="Submit" onclick="storeContriIDNLoad()"> </form>';
        
    }
    
}

var ContributersID;
var ContributersName;

function storeContriIDNLoad(){
    const ParentForm = document.querySelector("#AddEventDiv form");
    var checked = document.querySelectorAll('#AddEventDiv input[type="checkbox"]:checked');
    if(checked.length==0)alert("Select atleast one Contributer");
    else{
        ContributersID = Array.from(checked).map(function(option){
            return option.id;
        });
        ContributersName = Array.from(checked).map(function(option){

            return document.querySelector('label[for="' + option.id + '"]').textContent;
        })
        // console.log("ContributersID: "+ ContributersID);
        // console.log("ContributersName: "+ ContributersName);
        
        
        ParentForm.innerHTML="";
        ContributersName.forEach(function(item){
            const label = document.createElement('label');
            label.textContent = item;
            const input = document.createElement('input');
            input.type = 'number';
            input.name = item;
            input.required = true;
            ParentForm.appendChild(label);
            ParentForm.appendChild(input);
            ParentForm.append(document.createElement("br"));
        })
        const Submit = document.createElement('input');
        Submit.type = 'button';
        Submit.value = 'Submit';
        Submit.addEventListener("click",storeContriAmountNloadNsubmit)
        ParentForm.appendChild(Submit);
    }
}

var ContributersAmount;
function storeContriAmountNloadNsubmit(){

    var amount = document.querySelectorAll('#AddEventDiv input[type="number"]')
    ContributersAmount = Array.from(amount).map(function(option){
        return option.value;
    })
    // console.log("Amount for contributers: " + ContributersAmount)

    const ParentDiv = document.querySelector("#AddEventDiv");
    ParentDiv.innerHTML=`
    <button type="button" onclick="loadForm1()">Add Entry</button>
    `
    // console.log("entry recorded")
    alert("Expense Recorded in Database");

    const entry= new FormData();
    entry.append("PayeeID",PayeeID);
    entry.append("Amount",amount);
    entry.append("ContriID",ContributersID);
    entry.append("ContriAmt",ContributersAmount);
    entry.append("ExpDate",Math.floor(Date.now() / 1000));//UnixTimeStamp
    entry.append("ExpName",ExpName);
    entry.append("GrpID",GrpID);

    fetch('/add_expense',{
        method:'POST',
        body: entry
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
    

}

function loadForm2(){
    // console.log("Paymnet record initiated");
    const ParentDiv = document.querySelector("#AddPaymentDiv")
    ParentDiv.innerHTML=`
    <form>
        <label for="amount">Enter the Amount Paid:</label>
        <input type="number" id="amount" name="amount" required><br>
        <input type="button" value="Next" onclick="storeAmountNLoad2()">
    </form>
    `    
}

function storeAmountNLoad2() {
    const ParentDiv = document.querySelector("#AddPaymentDiv");
    amount = document.querySelector("#AddPaymentDiv #amount").value;
    console.log("The amount entered is: " + amount);
    ParentDiv.innerHTML=`
    <form >
        {% for group in groups %}
        <label for="{{ group[0] }}">{{ group[1] }}</label>
        <input type="radio" id="{{ group[0] }}" name="_"><br>
        {% endfor %}
        <input type="button" value="Next" onclick="storeGrpIDNLoad2()">
    </form>
    `
}

function storeGrpIDNLoad2(){
    const ParentDiv = document.querySelector("#AddPaymentDiv");
    var selected = document.querySelector('#AddPaymentDiv input[type="radio"]:checked');
    if(selected.length==0) alert("Select atleast one group");
    else{
        GrpID = selected.id;
        // console.log("Selected grp: " + GrpID);
        ParentDiv.innerHTML=`
        <form>
            {% for member in groups[2] %}
            <label for="{{ member[0] }}">{{ member[1] }}</label>
            <input type="radio" id="{{ member[0] }} name="_"><br>
            {% endfor %}
            <input type="button" value="Submit" onclick="storeDebterIDNSubmitNLoad()">
        </form>
        `
    }
    
}

var debterID;
function storeDebterIDNSubmitNLoad(){
    const ParentDiv = document.querySelector("#AddPaymentDiv");
    var selected = document.querySelector('#AddPaymentDiv input[type="radio"]:checked');
    if(selected.length==0) alert("Select a Person");
    else{
        debterID = selected.id;
        // console.log("Selected Debter: " + debterID);
        ParentDiv.innerHTML=`
        <button type="button" onclick="loadForm2()">Add Payment</button>
        `
        alert("Payment Recorded in Database");
        const entry= new FormData();
        entry.append("usr1ID",PayeeID);
        entry.append("usr2ID",debterID);
        entry.append("amount",amount);
        entry.append("PayDate",Math.floor(Date.now() / 1000));//UnixTimeStamp
        entry.append("GrpID",GrpID);

        fetch('/add_expense',{
            method:'POST',
            body: entry
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));

    }
}