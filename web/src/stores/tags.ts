import { defineStore } from 'pinia';
import axios from 'axios';

export const useTagStore = defineStore('tags', {
    state: () => ({
        createdTag: null,
        tags: [] as any[]
    }),
    actions: {
        createTag(tag) {
            this.createdTag = tag;
            console.log("store created tag: " + tag)
        },
        async fetchTags() {
            console.log("fetching tags");
            try {
                const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
                const response = await axios.get(`${apiBaseUrl}/tags`)
                const tags = response.data;
                this.tags = tags;
                return tags;
            } catch (error) {
                return [
                    { "tag": "Could", "resource_count": 1 },
                    { "tag": "Not", "resource_count": 2 },
                    { "tag": "Get", "resource_count": 3 },
                    { "tag": "Counts", "resource_count": 4 }
                ]
            }
        }
    }
});