function LoadForm(){
    console.log("Group Expense Entry Initiated");
    const ParentDiv = document.querySelector("#AddGrp")
    ParentDiv.innerHTML=`
    <form>
        <label for="name">Enter Group Name:</label>
        <input type="text" id="name" name="grpName" required><br>
        <input type="button" value="Next" onclick="storeGNameNLoad()">
    </form>
    `    
}

var GrpName;
function storeGNameNLoad(){
    GrpName = document.querySelector("#AddGrp #name").value;
    console.log("Name of New Grp: "+GrpName);
    const ParentDiv = document.querySelector("#AddGrp")
    ParentDiv.innerHTML=`
    <form>
        <label for="num">Enter Number of Members:</label>
        <input type="number" id="num" required><br>
        <input type="button" value="Next" onclick="storeNumNLoad()">
    </form>
    `    
}

var Num;
function storeNumNLoad(){
    Num = document.querySelector("#AddGrp #num").value;
    console.log("Number of Mem: "+Num);
    const ParentDiv = document.querySelector("#AddGrp");
    ParentDiv.innerHTML="";
    for(var i=0; i<Num; ++i){
        ParentDiv.innerHTML+="<label>Member-"+(i+1)+" Contact Number</label>"+"<input type='number' id ='"+i+"'required><br>"
    }
    ParentDiv.innerHTML+= '<input type="button" value="Next" onclick="storeMemNumNSubmit()">';
}

var MemNumber;
function storeMemNumNSubmit(){
    MemNumber = Array.from(document.querySelectorAll('#AddGrp input[type="number"]')).map(function(option){
        return option.value;
    })
    if(MemNumber.length == Num){
        console.log("Members Contacts: "+MemNumber);
        const ParentDiv = document.querySelector("#AddGrp");
        ParentDiv.innerHTML=`
        <button type="button" id="Add" onclick="LoadForm()">Make a Group</button>
        `
        console.log("grp added")
        alert("Group Added in Database");
    
        // In the python scipt make the make grp with passed grp name and add participant by itterating over mem contact list passed 
        const entry= new FormData();
        entry.append("GrpName",GrpName);
        // entry.append("MemNum",Num);
        entry.append("MemContact",MemNumber);
    
        fetch('/add_expense',{
            method:'POST',
            body: entry
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
    }
    else{
        alert("Enter Number for all members");
    }
}
