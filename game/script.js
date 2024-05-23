import './node_modules/axios/dist/axios.js';


const defaultUrl = "https://pure-tadpole-causal.ngrok-free.app";

async function fetchData(endpoint, data) {
  try {
    const response = await axios.post(`${defaultUrl}/${endpoint}`, data);
    return response.data;
  } catch (error) {
    console.log(error);
  }
}

let amountCounterChange = 1;

async function setUserBalance(userId) {
  const data = await fetchData("user/balance", {id: userId});
  console.log(data);
  amountCounterChange = amountCounterChange * parseInt(data["multiplier"]);
  document.querySelector('#counter').innerHTML = data["balance"];
}

async function mountBalance(userId) {
  const counter = document.querySelector('#counter');
  const data = await fetchData("user/balance/mount", {id: userId, balance: parseInt(counter.innerHTML)});
  console.log(data);
}

document.addEventListener('DOMContentLoaded', function() {
  const tg = window.Telegram.WebApp;
  const userId = tg.initDataUnsafe.user.id;
  (async function() {
    await setUserBalance(userId);
  })()
  setInterval(function () {
    (async function () {
      await mountBalance(userId);
    })()
  }, 5000)
  const container = document.querySelector('.container');
  const sound = new Howl({
    src: ['sound.mp3']
  });
  
  function createNewImage() {
    const newImage = document.createElement('img');
    const images = ['image1.png', 'image2.png', 'image3.png'];
    newImage.src = images[Math.floor(Math.random() * images.length)];
    newImage.classList.add('draggable');
    newImage.id = 'image' + (document.querySelectorAll('.draggable').length + 1);
    newImage.style.top = '70%';
    newImage.style.left = '-20px';
    container.appendChild(newImage);
    makeDraggable(newImage);
    const sound = new Howl({src: ['sound.mp3']});
  }

  function makeDraggable(image) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

    image.addEventListener('mousedown', dragMouseDown);
    image.addEventListener('touchstart', dragMouseDown);
    const sound = new Howl({src: ['sound.mp3']});

    function dragMouseDown(e) {
      e = e || window.event;
      e.preventDefault();
      pos3 = e.type === 'touchstart' ? e.touches[0].clientX : e.clientX;
      pos4 = e.type === 'touchstart' ? e.touches[0].clientY : e.clientY;
      document.onmouseup = closeDragElement;
      document.onmousemove = elementDrag;
      document.ontouchmove = elementDrag;
    }

    function elementDrag(e) {
      e = e || window.event;
      e.preventDefault();
      pos1 = pos3 - (e.type === 'touchmove' ? e.touches[0].clientX : e.clientX);
      pos2 = pos4 - (e.type === 'touchmove' ? e.touches[0].clientY : e.clientY);
      pos3 = e.type === 'touchmove' ? e.touches[0].clientX : e.clientX;
      pos4 = e.type === 'touchmove' ? e.touches[0].clientY : e.clientY;
      image.style.top = (image.offsetTop - pos2) + "px";
      image.style.left = (image.offsetLeft - pos1) + "px";

      if ((image.offsetLeft + image.offsetWidth / 2) >= (container.offsetLeft + container.offsetWidth / 1.25)) {
        image.style.display = 'none';
        image.remove();
        const counter = document.querySelector('#counter');
        counter.innerHTML = parseInt(counter.innerHTML) + amountCounterChange;
        sound.play();
        createNewImage();
      }
    }

    function closeDragElement() {
      document.onmouseup = null;
      document.onmousemove = null;
      document.ontouchmove = null;
    }
  }

  const initialImage = document.querySelector('.draggable');
  makeDraggable(initialImage, 1);

  document.addEventListener('click', function() {
    const introImage = document.getElementById('intro-image');
    if (introImage) {
      introImage.style.display = 'none';
    }
  });
});