function valueChange(event) {
  console.log('選択されているのは ' + event.currentTarget.value + ' です');
  event.target.parentElement.querySelector("input[type=text]:nth-child(6)").value = "8";
  event.target.parentElement.querySelector("input[type=text]:nth-child(7)").value = "0";
  event.target.parentElement.querySelector("input[type=text]:nth-child(8)").value = "17";
  event.target.parentElement.querySelector("input[type=text]:nth-child(9)").value = "0";
  event.target.parentElement.querySelector("input[type=text]:nth-child(10)").value = "12";
  event.target.parentElement.querySelector("input[type=text]:nth-child(11)").value = "0";
  event.target.parentElement.querySelector("input[type=text]:nth-child(12)").value = "13";
  event.target.parentElement.querySelector("input[type=text]:nth-child(13)").value = "0";
}

function valueChange(event) {
  console.log('選択されているのは ' + event.currentTarget.value + ' です');
  var target = event.target;
  var parent = target.parentElement;//parent of "target"
  console.log(parent)
  parent.querySelector("input[type=text]:nth-child(6)").value = "8";
  parent.querySelector("input[type=text]:nth-child(7)").value = "0";
  parent.querySelector("input[type=text]:nth-child(8)").value = "17";
  parent.querySelector("input[type=text]:nth-child(9)").value = "0";
  parent.querySelector("input[type=text]:nth-child(10)").value = "12";
  parent.querySelector("input[type=text]:nth-child(11)").value = "0";
  parent.querySelector("input[type=text]:nth-child(12)").value = "13";
  parent.querySelector("input[type=text]:nth-child(13)").value = "0";
}
let el = document.querySelectorAll("input[type=radio]:nth-child(5)")
el.forEach(x=> x.addEventListener('change', valueChange))

javascript:(function(){
  function valueChange(event) {
    console.log('選択されているのは ' + event.currentTarget.value + ' です');
    var target = event.target;
    var parent = target.parentElement;
    parent.querySelector("input[type=text]:nth-child(6)").value = "8";
    parent.querySelector("input[type=text]:nth-child(7)").value = "0";
    parent.querySelector("input[type=text]:nth-child(8)").value = "17";
    parent.querySelector("input[type=text]:nth-child(9)").value = "0";
    parent.querySelector("input[type=text]:nth-child(10)").value = "12";
    parent.querySelector("input[type=text]:nth-child(11)").value = "0";
    parent.querySelector("input[type=text]:nth-child(12)").value = "13";
    parent.querySelector("input[type=text]:nth-child(13)").value = "0";
  }
  var el = document.querySelectorAll("input[type=radio]:nth-child(5)");
  el.forEach(x=> x.addEventListener('change', valueChange))
})()