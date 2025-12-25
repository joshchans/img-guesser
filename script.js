const imgEl = document.getElementById("img");
const revealBtn = document.getElementById("revealBtn");
const nextBtn = document.getElementById("nextBtn");
const answerEl = document.getElementById("answer");
const clueBtn = document.getElementById("clueBtn");
const ZOOM_LEVELS = [8, 7, 6, 5, 4, 3, 2, 1];
let zoomIndex = 0;

let images = [];
let current = null;
let revealed = false;

function prettify(filename){
  return filename
    .replace(/\.[^.]+$/, "")
    .replace(/[_-]+/g, " ")
    .trim();
}

function rand(min, max){
  return Math.random() * (max - min) + min;
}

function zoomIn(){
  imgEl.style.transformOrigin =
    `${rand(20,80)}% ${rand(20,80)}%`;
  imgEl.style.transform = "scale(7.5)";
}

function zoomOut(){
  imgEl.style.transformOrigin = "center";
  imgEl.style.transform = "scale(1)";
}

function newRound(){
  revealed = false;
  answerEl.hidden = true;
  zoomIn();
}

function reveal(){
  if (revealed) return;
  revealed = true;

  zoomIndex = ZOOM_LEVELS.length - 1;

  // Zoom out from the SAME focal point
  imgEl.style.transform = "scale(1)";

  imgEl.addEventListener(
    "transitionend",
    () => {
      // Hide for a single layout change
      imgEl.style.opacity = "0";

      // Next frame: switch layout safely
      requestAnimationFrame(() => {
        imgEl.style.objectFit = "contain";

        // Show again
        requestAnimationFrame(() => {
          imgEl.style.opacity = "1";
        });
      });
    },
    { once: true }
  );

  answerEl.textContent = `🎁 ${current.label}`;
  answerEl.hidden = false;
}
function next(){
  current = images[Math.floor(Math.random() * images.length)];

  revealed = false;
  zoomIndex = 0;
  answerEl.hidden = true;

  imgEl.style.transition = "none";
  imgEl.style.opacity = "1";
  imgEl.style.transform = `scale(${ZOOM_LEVELS[zoomIndex]})`;
  imgEl.style.transformOrigin = "50% 50%";
  imgEl.style.visibility = "hidden";
  imgEl.style.objectFit = "cover";
  
  imgEl.src = `images/${current.file}`;

  imgEl.onload = () => {
    const ox = rand(20, 80);
    const oy = rand(20, 80);
    imgEl.style.transformOrigin = `${ox}% ${oy}%`;

    imgEl.style.transition = "transform 1s ease";
    imgEl.style.visibility = "visible";
  };
}

function clue(){
  if (revealed) return;

  if (zoomIndex < ZOOM_LEVELS.length - 1) {
    zoomIndex++;
    imgEl.style.transform = `scale(${ZOOM_LEVELS[zoomIndex]})`;
  }
}

async function loadImages(){
  const res = await fetch("images.json", { cache: "no-store" });
  images = (await res.json()).map(f => ({
    file: f,
    label: prettify(f)
  }));
  next();
}

revealBtn.onclick = reveal;
nextBtn.onclick = next;
clueBtn.onclick = clue;

loadImages();
