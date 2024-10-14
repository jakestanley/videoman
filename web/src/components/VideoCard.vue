<template>
  <div class="video-card">
    <video class="video-element" autoplay loop :src="videoUrl">{{ relative_path }}</video>
    <button class="btn btn-delete" onclick="deleteVideo('${video.id}')">Delete</button>
    <div class="tags">
      <h1>Tags</h1>
      <ul>
        <li v-for="(item, index) in tags" :key="index">
          {{ item }} <button class="btn btn-delete-tag">Delete</button>
        </li>
      </ul>
      
      <div class="input-section">
        <input type="text" v-model="tagText" @keyup.enter="submitTag" placeholder="Create a tag"/>
      </div>

      <h1>Suggested tags</h1>
      <ul>
        <li v-for="(item, index) in suggestedTags" :key="index">
          <a href="#" @click="tagVideo(item)">{{ item.tag }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

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
  data() {
    return {
      tagText: '', // Holds the value of the text input
    };
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
            .replace(/[\[\]\\]/g, '') // Remove square brackets
            .split(/[\/ ]+/) // Split by slashes or spaces
            .map(item => item.replace(fileExtensionRegex, '')) // Remove file extensions if present
            .filter(item => !isoDateRegex.test(item)) // Exclude ISO formatted dates
            .filter(item => !isoTimeRegex.test(item)) // Exclude ISO formatted times
            .filter(item => !uuidRegex.test(item)) // Exclude UUIDs)
        )
      ).filter(item => !this.tags.includes(item.toLowerCase()));

      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
      const tags = result.map(item => {
        return {
          tag: item,
          url: apiBaseUrl + "/videos/" + this.id + "/tags/" + item
        };
      });

      return tags;
    }
  },
  methods: {
    submitTag() {
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
      const url = apiBaseUrl + "/videos/" + this.id + "/tags/" + this.tagText
      axios.post(url)
      console.log("Submitted tag", this.tagText)
    },
    tagVideo(item) {
      axios.post(item.url)
      console.log('Item clicked', item);
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
  max-width: 300px; /* Set your desired max width */
  width: 100%;      /* Ensures the card fills its container */
}

h1 {
  font-size: medium;
  font-weight: bold;
  color: black;
}

p, li {
  color: black;
}
ul {
  list-style: none;
  list-style-type: none;
}
li {
  list-style: none;
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
