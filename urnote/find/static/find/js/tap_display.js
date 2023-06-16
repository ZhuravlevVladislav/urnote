function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', (event) => {
    let rhythmData = [];
    let lastHitTime = null;
    let maxTimeBetweenHits = 2000;
    let rhythmArea = document.querySelector('#rhythm-area');
    let lastSquareRight = 0;
    let lastSquareBottom = 0;
    let isFirstHit = true;

    window.addEventListener('keydown', function (e) {
        if (e.code === 'Space') {
            e.preventDefault();

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
                square.style.left = '0px';
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
            lastSquareRight += 20 + transparentBlockWidth;

            rhythmData.push(currentTime);
            lastHitTime = currentTime;
        }
    });

    document.querySelector('#find-button').addEventListener('click', function () {
        fetch('/find/api/rhythm/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({rhythm_data: rhythmData})
        })
            .then(response => response.json())
            .then(data => {
                let resultsDiv = document.querySelector('#results');
                resultsDiv.innerHTML = '';



                if (Array.isArray(data)) {
                    let ul = document.createElement('ul');
                    ul.classList.add('song-list');

                    data.forEach(song => {
                        let li = document.createElement('li');
                        li.classList.add('song-item');

                        let fullTitleDiv = document.createElement('div');
                        fullTitleDiv.classList.add('full-title');
                        fullTitleDiv.textContent = song.artist + ' - ' + song.title

                        let linkDiv = document.createElement('div');
                        linkDiv.classList.add('song-link');
                        let link = document.createElement('a');
                        link.href = song.youtube_link;
                        link.textContent = 'Listen on YouTube';
                        link.target = '_blank';
                        linkDiv.appendChild(link);

                        li.append(fullTitleDiv)
                        li.appendChild(linkDiv);
                        ul.appendChild(li);
                    });

                    resultsDiv.appendChild(ul);
                } else {
                    resultsDiv.textContent = 'По вашему запросу ничего не найдено'
                    resultsDiv.style.color = 'white';
                }
            })
            .catch(error => console.error('Error:', error));
    });
});
