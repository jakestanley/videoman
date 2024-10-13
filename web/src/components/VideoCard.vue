<template>
  <div class="video-card">
    <video class="video-element" autoplay loop :src="videoUrl"></video>
    <!-- <p>{{ relative_path }}</p> -->
    <div class="buttons">
      <button class="btn btn-delete" onclick="deleteVideo('${video.id}')">Delete</button>
      <button class="btn btn-tag" onclick="openTagModal('${video.id}')">Tag</button>
    </div>
    <div class="tags">
      <p>Tags</p>
      <ul>
        <li v-for="(item, index) in tags" :key="index">
          {{ item }}
        </li>
      </ul>
      <p>Suggested tags</p>
      <ul>
        <li v-for="(item, index) in suggestedTags" :key="index">
          {{ item }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VideoCard',
  props: {
    id: {
        type: String,
        required: true
    },
    relative_path: {
      type: String,
      required: false,
      default: 'no path'
    },
    contents_hash: {
      type: String,
      default: 'no hash'
    },
    tags: {
      type: Array,
      required: false,
      default: ["tag"]
    }
  },
  computed: {
    videoUrl() {
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
      return `${apiBaseUrl}/assets/${this.contents_hash}.webm`
    },
    suggestedTags() {

      const isoDateRegex = /^\d{4}-\d{2}-\d{2}$/; // Regex to match ISO formatted dates
      const isoTimeRegex = /^\d{2}_\d{2}$/; // Regex to match ISO formatted dates
      const fileExtensionRegex = /\.[^\/.]+$/; // Regex to match a file extension
      const uuidRegex = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/; // Regex to match UUIDs

      const result = Array.from(
        new Set(
          this.relative_path
            .replace(/[\[\]]/g, '') // Remove square brackets
            .split(/[\/ ]+/) // Split by slashes or spaces
            .map(item => item.replace(fileExtensionRegex, '')) // Remove file extensions if present
            .filter(item => !isoDateRegex.test(item)) // Exclude ISO formatted dates
            .filter(item => !isoTimeRegex.test(item)) // Exclude ISO formatted times
            .filter(item => !uuidRegex.test(item)) // Exclude UUIDs)
        )
      ).filter(item => !this.tags.includes(item));

      return result;
    }
  }
}
</script>

<style scoped>
.video-card {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
}

p, li {
  color: black;
}

.video-element {
  width: 100%;
  height: auto;
  border-radius: 4px;
}

.video-text {
  margin-top: 10px;
}

.video-text h3 {
  margin: 0;
  font-size: 1.2em;
}

.video-text p {
  margin: 5px 0 0;
  color: #555;
}
</style>
