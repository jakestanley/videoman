document.addEventListener('DOMContentLoaded', loadVideos);

async function loadVideos() {
  const response = await fetch('/videos');
  const videos = await response.json();

  const videoGrid = document.getElementById('videoGrid');
  videos.forEach(video => {
    const videoItem = document.createElement('div');
    videoItem.classList.add('video-item');
    videoItem.innerHTML = `
      <video class="video-thumbnail" autoplay loop muted src="${video.thumbnailUrl}" data-video-id="${video.id}"></video>
      <div class="tag-container">
        ${video.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
      </div>
      <div class="buttons">
        <button class="btn btn-delete" onclick="deleteVideo('${video.id}')">Delete</button>
        <button class="btn btn-tag" onclick="openTagModal('${video.id}')">Tag</button>
      </div>
    `;
    videoGrid.appendChild(videoItem);
  });
}

function deleteVideo(videoId) {
  fetch(`/delete-video`, {
    method: 'DELETE',
    body: JSON.stringify({ id: videoId }),
    headers: { 'Content-Type': 'application/json' }
  }).then(() => {
    document.location.reload();
  });
}

function openTagModal(videoId) {
  const tagModal = document.getElementById('tagModal');
  tagModal.style.display = 'block';
  tagModal.dataset.videoId = videoId;
}

function addTag() {
  const videoId = document.getElementById('tagModal').dataset.videoId;
  const tag = document.getElementById('tagInput').value;
  
  fetch(`/add-tag`, {
    method: 'POST',
    body: JSON.stringify({ id: videoId, tag }),
    headers: { 'Content-Type': 'application/json' }
  }).then(() => {
    document.location.reload();
  });
}
