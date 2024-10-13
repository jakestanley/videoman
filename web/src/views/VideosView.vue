<template>
  <div class="videos">
    <h1>This the videos page</h1>
    <div class="video-grid">
      <VideoCard
        v-for="(video, index) in videos"
        :key="index"
        :contents_hash="video.contents_hash"
        :id="video.id"
        :relative_path="video.relative_path"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import VideoCard from '../components/VideoCard.vue'

export default {
  name: 'Videos',
  components: {
    VideoCard
  },
  data() {
    return {
      videos: []
    }
  },
  created() {
    this.fetchVideos()
  },
  methods: {
    async fetchVideos() {
      try {
        const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
        const response = await axios.get(`${apiBaseUrl}/videos`)
        this.videos = response.data.map((video) => ({
          ...video,
          src: `http://localhost:5000/assets/${video.contents_hash}.webm`
        }));
      } catch (error) {
        console.error('Error fetching videos: ', error)
      }
    }
  }
}
</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-gap: 20px;
}
</style>
