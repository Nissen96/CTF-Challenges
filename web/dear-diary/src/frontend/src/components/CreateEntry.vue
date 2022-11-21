<script>
export default {
  data() {
    return {
      title: "",
      content: "",
      visibility: "public",
      errorText: "",
    };
  },
  computed: {
    authorized() {
      return this.$store.state.authorized_user !== null;
    },
  },
  methods: {
    async create() {
      await this.$http
        .post(
          "/api/entries",
          {
            title: this.title,
            content: this.content,
            is_public: this.visibility === "public",
          },
          {
            headers: {
              Authorization: this.$cookies.isKey("token")
                ? "Bearer " + this.$cookies.get("token")
                : undefined,
            },
          }
        )
        .then(() => {
          this.errorText = "";
          this.$emit("refetch");
        })
        .catch((error) => {
          this.errorText = error.response.data
            ? error.response.data.detail
            : "Something went wrong";
        });
    },
  },
};
</script>

<template>
  <h3>Add Entry</h3>
  <div v-if="$store.state.authorized_user">
    <input v-model="title" type="text" placeholder="Title" required />
    <br />
    <textarea
      v-model="content"
      style="margin: 10px 0"
      placeholder="Content"
      required
    ></textarea>
    <br />
    <input type="radio" id="public" value="public" v-model="visibility" />
    <label for="public">🌐 Public</label>
    &nbsp;
    <input type="radio" id="private" value="private" v-model="visibility" />
    <label for="private">🔒 Private</label>
    <br />
    <button @click="create">Upload</button>
    <div class="error">
      <small>{{ errorText }}</small>
    </div>
  </div>
  <div v-else style="margin-top: 3em">
    <h5>Please <a @click="$emit('login')">login</a> to upload new entries</h5>
  </div>
</template>

<style scoped>
button {
  margin: 20px 0;
}
</style>
