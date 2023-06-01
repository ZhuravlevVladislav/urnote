document.addEventListener('DOMContentLoaded', (event) => {
    let rhythmData = [];
    let lastHitTime = null;  // Initialize to null
    let maxTimeBetweenHits = 2000;  // Maximum time between hits in milliseconds
    let rhythmArea = document.querySelector('#rhythm-area');
    let lastSquareRight = 0;
    let lastSquareBottom = 0;
    let isFirstHit = true;

    window.addEventListener('keydown', function(e) {
      if (e.code === 'Space') {  // Check if spacebar is pressed
        e.preventDefault();  // Prevent the default action (scroll)

        let currentTime = new Date().getTime();
        let square = document.createElement('div');
        square.classList.add('square');
        square.style.top = lastSquareBottom + 'px';

        let transparentBlockWidth = 0;
        if (lastHitTime) {
          let timeBetweenHits = currentTime - lastHitTime;
          transparentBlockWidth = timeBetweenHits / maxTimeBetweenHits * (rhythmArea.offsetWidth - 20);
          square.style.left = lastSquareRight + transparentBlockWidth + 'px';
        } else if (isFirstHit) {
          square.style.left = '0px';  // Special case for the first square
          isFirstHit = false;
        }

        if (parseInt(square.style.left) + 20 > rhythmArea.offsetWidth) {
          lastSquareRight = 0;
          lastSquareBottom += 20;
          square.style.top = lastSquareBottom + 'px';
          square.style.left = lastSquareRight + transparentBlockWidth + 'px';
        } else {
          lastSquareRight = parseInt(square.style.left);
        }

        rhythmArea.appendChild(square);
        lastSquareRight += 20 + transparentBlockWidth; // include transparent block width

        rhythmData.push(currentTime);
        lastHitTime = currentTime;
      }
    });

    document.querySelector('#find-button').addEventListener('click', function() {
      fetch('/api/rhythm/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(rhythmData)
      });
    });
});
