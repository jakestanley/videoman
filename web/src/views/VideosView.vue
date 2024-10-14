<template>
  <div class="videos">
    <h1>Videoman</h1>
    <button class="btn" @click="previousPage()">Previous page</button>
    <button class="btn" @click="nextPage()">Next page</button>
    <div class="video-grid">
      <VideoCard
        v-for="(video, index) in videos"
        :key="index"
        :contents_hash="video.contents_hash"
        :id="video.id"
        :relative_path="video.relative_path"
        :tags="video.tags"
        :created_date="video.created"
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
      videos: [],
      tag: "",
      page: 0
    }
  },
  created() {
    this.fetchVideos()
  },
  watch: { // TODO how can i load this on mount?
    '$route.query.tag': {
      immediate: true,
      handler(newTag, oldTag) {
        this.tag = newTag;
        this.fetchVideosByTag(newTag);
      },
    },
    '$route.query.page': {
      immediate: true,
      handler(newPage, oldPage) {
        if (newPage != oldPage) {
          this.fetchVideosByTag(this.tag)
          console.log("will fetch page " + newPage)
        }
      }
    }
  },
  methods: {
    async nextPage() {
      this.page++
      const page = this.page;
      this.$router.push({
        query: {
          ...this.$route.query, // Keep the existing query parameters
          page // Add or update the new parameter
        },
      });
    },
    async previousPage() {
      this.page--
      if (this.page < 0) {
        this.page = 0;
      }
      const page = this.page;
      this.$router.push({
        query: {
          ...this.$route.query, // Keep the existing query parameters
          page // Add or update the new parameter
        },
      });
    },
    async fetchVideos() {
      try {
        const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
        const response = await axios.get(`${apiBaseUrl}/videos`, {
          params: {
            page: this.page
          }
        })
        this.videos = response.data.map((video) => ({
          ...video,
          src: `${apiBaseUrl}/assets/${video.contents_hash}.webm`
        }));
      } catch (error) {
        console.error('Error fetching videos: ', error)
      }
    },
    async fetchVideosByTag(tag) {
      // TODO use this.tag so we can reuse fetchVideos
      if (tag == undefined) {
        this.fetchVideos()
        return
      }
      try {
        const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
        const response = await axios.get(`${apiBaseUrl}/tags/${tag}/videos`, {
          params: {
            page: this.page
          }
        })
        this.videos = response.data.map((video) => ({
          ...video,
          src: `${apiBaseUrl}/assets/${video.contents_hash}.webm`
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
