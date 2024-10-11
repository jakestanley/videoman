<template>
  <div class="video-card">
    <video class="video-element" autoplay :src="videoSrc"></video>
    <div class="video-text">
      <h3>{{ title }}</h3>
      <p>{{ description }}</p>
      <p>{{ id }}</p>
      <p>{{ relative_path }}</p>
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
    src: {
        type: String,
        required: false
    },
    description: {
      type: String,
      default: 'No description available.'
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
