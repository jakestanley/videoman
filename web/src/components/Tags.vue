<template>
  <div class="greetings">
    <h1 class="green">Tags</h1>
    <ul>
      <p>
        <a href="#" @click.prevent=filterClear()>Clear</a>
      </p>
      <li v-for="(item, index) in tags" :key="index">
        <a href="#" @click.prevent=filterVideos(item.tag)>{{ item.tag }} ({{item.resource_count}})</a>
      </li>
    </ul>
  </div>
</template>

<script>
import { useTagStore } from '@/stores/tags';
import { watch } from 'vue';

export default {
  name: 'Tags',
  watch: {
    'tagStore.createdTag': {
      handler(newTag) {
        console.log('Tag created:', newTag);
        this.fetchTags();
      },
      immediate: true,
    },
  },
  computed: {
    tagStore() {
      return useTagStore();
    }
  },
  created() {
    this.fetchTags()
  },
  data() {
    return {
      tags: []
    }
  },
  methods: {
    async fetchTags() {
      this.tagStore
        .fetchTags()
        .then(tags => this.tags = tags);
    },
    async filterVideos(tag) {
      console.log("filtering on " + tag)
      this.$router.push({ query: { tag } });
    },
    async filterClear() {
      this.$router.push({ query: {} });
    }
  }
}
</script>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 256px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
