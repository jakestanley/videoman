<template>
  <div class="video-card">
    <video class="video-element" controls :src="videoSrc"></video>
    <div class="video-text">
      <h3>{{ title }}</h3>
      <p>{{ description }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VideoCard',
  props: {
    videoSrc: {
      type: String,
      required: true
    },
    title: {
      type: String,
      default: 'Untitled Video'
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
