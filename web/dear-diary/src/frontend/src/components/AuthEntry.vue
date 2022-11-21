<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      errorText: "",
      action: "login",
    };
  },
  methods: {
    async login() {
      try {
        let resp = await this.$http.post("/api/login", {
          username: this.username,
          password: this.password,
        });
        this.$cookies.set("token", resp.data.access_token);
        resp = await this.$http.get("/api/users/me", {
          headers: {
            Authorization: this.$cookies.isKey("token")
              ? "Bearer " + this.$cookies.get("token")
              : undefined,
          },
        });
        this.$store.commit("login", resp.data.username);
        this.errorText = "";
        this.$emit("refetch");
      } catch (error) {
        this.errorText = error.response.data
          ? error.response.data.detail
          : "Something went wrong";
        this.$cookies.remove("token");
        this.$store.commit("logout");
      }
    },
    logout() {
      this.username = "";
      this.password = "";
      this.errorText = "";
      this.$cookies.remove("token");
      this.$store.commit("logout");
      this.$emit("refetch");
    },
    async register() {
      await this.$http
        .post("/api/users", {
          username: this.username,
          password: this.password,
        })
        .then(async () => {
          this.errorText = "";
          await this.login();
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
  <div v-if="$store.state.authorized_user">
    <h2>Welcome</h2>
    <h5>{{ this.$store.state.authorized_user }}</h5>
    <p>
      Turn the pages to read your own diary entries and all public entries. Flip
      to the <a @click="$emit('createentry')">last page</a> to add a new entry.
    </p>
    <button @click="logout">logout</button>
  </div>
  <div v-else>
    <h2 v-if="action === 'login'">Sign in</h2>
    <h2 v-else-if="action === 'register'">Register</h2>
    <input v-model="username" type="text" placeholder="Username" required />
    <br />
    <input v-model="password" type="password" placeholder="Password" required />
    <div v-if="action === 'login'">
      <button @click="login">login</button>
      <div>
        <small>
          <a
            @click="
              errorText = '';
              action = 'register';
            "
            >Register here</a
          >
        </small>
      </div>
    </div>
    <div v-else-if="action === 'register'">
      <button @click="register">register</button>
      <div>
        <small>
          <a
            @click="
              errorText = '';
              action = 'login';
            "
            >Login here</a
          >
        </small>
      </div>
    </div>
  </div>
  <div class="error">
    <small>{{ errorText }}</small>
  </div>
</template>

<style scoped></style>
