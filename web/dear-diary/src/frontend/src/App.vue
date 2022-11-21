<script>
import TheDiary from "./components/TheDiary.vue";

export default {
  components: {
    TheDiary,
  },
  async created() {
    try {
      const resp = await this.$http.get("/api/users/me", {
        headers: {
          Authorization: this.$cookies.isKey("token")
            ? "Bearer " + this.$cookies.get("token")
            : undefined,
        },
      });
      this.$store.commit("login", resp.data.username);
    } catch {
      this.$store.commit("logout");
    }
  },
};
</script>

<template>
  <TheDiary />
</template>

<style>
#app {
  height: 100%;
  margin: 0 auto;
  font-weight: normal;
}
</style>
