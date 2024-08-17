let valueDisplays = document.querySelectorAll(".num");
let interval = 4000;

valueDisplays.forEach((valueDisplay) => {
  let startValue = 0;
  let thatValue = valueDisplay.getAttribute("data-val");
  let extraChar = '';
  if(thatValue.charAt(thatValue.length - 1) === 'M'){
    extraChar = 'M';
    thatValue = thatValue.slice(0 , thatValue.length - 1);
  }

  console.log("Value is " + thatValue);
  let endValue = parseInt(thatValue);
  let duration = Math.floor(interval / endValue);
  let counter = setInterval(function () {
    startValue += 1;
    
    valueDisplay.textContent =startValue.toString() + extraChar;
    if (startValue == endValue) {
      clearInterval(counter);
    }
  }, duration);
});