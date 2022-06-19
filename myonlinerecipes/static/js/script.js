
/**
 * help the user to understand if the recipes will be private or public
 */
const privateSwitch =()=>{
   let myswitch = document.getElementById("switch")
    if(myswitch.checked === false){
        document.getElementById("switch-label").innerHTML = 'Private'
    }else{
        document.getElementById("switch-label").innerHTML = 'Public'
    }
}