<template>
  <div>
    <h1 class="green">Tags</h1>
    <button @click.prevent=sortTagsAlphabetically()>Sort by name</button>
    <button @click.prevent=sortTagsCount()>Sort by count</button>
    <input type="text" v-model="filterText" @keyup.enter="filterTags" placeholder="Filter tags"/>
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
      tags: [],
      filterText: ""
    }
  },
  // TODO: pin video for when comparing with other tags
  // TODO: fuzzy search existing and present on suggested tags
  methods: {
    async fetchTags() {
      this.tagStore
        .fetchTags()
        .then(tags => this.tags = tags);
    },
    async filterVideos(tag) {
      this.$router.push({ query: { tag } });
    },
    async filterClear() {
      this.$router.push({ query: {} });
    },
    async sortTagsAlphabetically() {
      console.log("sorting tags")
      this.tags.sort((a, b) => a.tag.localeCompare(b.tag));
    },
    async sortTagsCount() {
      this.tags.sort((a, b) => a.resource_count < b.resource_count);
    },
    async filterTags() {
      console.log("filtering tags on " + this.filterText)
      this.tagStore.fetchTags().then(tags => {
        this.tags = tags.filter(item => item.tag.includes(this.filterText));
      })
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
