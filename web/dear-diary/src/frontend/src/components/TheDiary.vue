<script>
import AuthEntry from "./AuthEntry.vue";
import CreateEntry from "./CreateEntry.vue";

export default {
  components: {
    AuthEntry,
    CreateEntry,
  },
  data() {
    return {
      entries: [],
    };
  },
  async mounted() {
    await this.getEntries();
    $("#flipbook").turn({ duration: 2000 });
  },
  methods: {
    async getEntries() {
      await this.$http
        .get("/api/entries", {
          headers: {
            Authorization: this.$cookies.isKey("token")
              ? "Bearer " + this.$cookies.get("token")
              : undefined,
          },
        })
        .then((response) => {
          this.entries = response.data.map((entry) => ({
            title: entry.title,
            content: entry.content,
            author: entry.author_name,
            isPublic: entry.is_public,
          }));
        })
        .catch(async () => {
          if (this.$cookies.isKey("token")) {
            this.$cookies.remove("token");
            this.$store.commit("logout");
            await this.getEntries();
          }
        });
    },
    refetch() {
      window.location.reload();
    },
    flipToLogin() {
      $("#flipbook").turn("page", 2);
    },
    flipToCreate() {
      $("#flipbook").turn("page", $("#flipbook").turn("pages") - 3);
    },
  },
};
</script>

<template>
  <div id="flipbook">
    <div id="front" class="hard">
      <h1 style="margin: 30% 0 0">Diary</h1>
      <i style="font-size: 2.5em">♥</i>
    </div>
    <div class="hard"></div>
    <div>
      <div class="contentpage">
        <AuthEntry @refetch="refetch" @createentry="flipToCreate" />
      </div>
    </div>
    <template v-for="(entry, index) in entries" :key="index">
      <div>
        <div class="titlepage">
          <h2>{{ entry.title }}</h2>
          <small>
            <em> By {{ entry.author }} </em>
          </small>
          <p v-if="entry.isPublic">🌐</p>
          <p v-else>🔒</p>
        </div>
      </div>
      <div>
        <div class="contentpage">
          <p style="white-space: pre-line">{{ entry.content }}</p>
        </div>
      </div>
    </template>

    <div>
      <div class="titlepage">
        <h2>The End</h2>
      </div>
    </div>
    <div>
      <div class="contentpage">
        <CreateEntry @refetch="refetch" @login="flipToLogin" />
      </div>
    </div>

    <div></div>
    <div class="hard"></div>
    <div id="back" class="hard"></div>
  </div>
</template>

<style scoped>
.titlepage {
  padding: 30% 10%;
}

.contentpage {
  padding: 10%;
  word-wrap: break-word;
}

#flipbook {
  position: absolute !important;
  top: 30%;
  left: 30%;
  width: 55%;
  height: 65%;
}

#flipbook .page {
  background-color: #ffefed;
  font-size: 2em;
  text-align: center;
}

#flipbook .page-wrapper {
  -webkit-perspective: 2000px;
  -moz-perspective: 2000px;
  -ms-perspective: 2000px;
  -o-perspective: 2000px;
  perspective: 2000px;
}

#flipbook .hard {
  background: #ffbfc3 !important;
  -webkit-box-shadow: inset 0 0 10px #faa7ac !important;
  -moz-box-shadow: inset 0 0 10px #faa7ac !important;
  -o-box-shadow: inset 0 0 10px #faa7ac !important;
  -ms-box-shadow: inset 0 0 10px #faa7ac !important;
  box-shadow: inset 0 0 10px #faa7ac !important;
  font-weight: bold;
}

#flipbook #front {
  -webkit-box-shadow: inset 20px 0 5px #f3a7ac !important;
  -moz-box-shadow: inset 20px 0 5px #f3a7ac !important;
  -o-box-shadow: inset 20px 0 5px #f3a7ac !important;
  -ms-box-shadow: inset 20px 0 5px #f3a7ac !important;
  box-shadow: inset 20px 0 5px #f3a7ac !important;
}

#flipbook #back {
  -webkit-box-shadow: inset -20px 0 5px #f3a7ac !important;
  -moz-box-shadow: inset -20px 0 5px #f3a7ac !important;
  -o-box-shadow: inset -20px 0 5px #f3a7ac !important;
  -ms-box-shadow: inset -20px 0 5px #f3a7ac !important;
  box-shadow: inset -20px 0 5px #f3a7ac !important;
}

#flipbook .odd {
  background: -webkit-gradient(
    linear,
    right top,
    left top,
    color-stop(0.95, #ffefed),
    color-stop(1, #fbcfc9)
  );
  background-image: -webkit-linear-gradient(right, #ffefed 95%, #fbcfc9 100%);
  background-image: -moz-linear-gradient(right, #ffefed 95%, #fbcfc9 100%);
  background-image: -ms-linear-gradient(right, #ffefedff 95%, #fbcfc9 100%);
  background-image: -o-linear-gradient(right, #ffefed 95%, #fbcfc9 100%);
  background-image: linear-gradient(right, #ffefed 95%, #fbcfc9 100%);
  -webkit-box-shadow: inset 0 0 10px #fee4fc;
  -moz-box-shadow: inset 0 0 10px #fee4fc;
  -o-box-shadow: inset 0 0 10px #fee4fc;
  -ms-box-shadow: inset 0 0 10px #fee4fc;
  box-shadow: inset 0 0 10px #fee4fc;
}

#flipbook .even {
  background: -webkit-gradient(
    linear,
    left top,
    right top,
    color-stop(0.95, #ffefed),
    color-stop(1, #fbcfc9)
  );
  background-image: -webkit-linear-gradient(left, #ffefed 95%, #fbcfc9 100%);
  background-image: -moz-linear-gradient(left, #ffefed 95%, #fbcfc9 100%);
  background-image: -ms-linear-gradient(left, #ffefed 95%, #fbcfc9 100%);
  background-image: -o-linear-gradient(left, #ffefed 95%, #fbcfc9 100%);
  background-image: linear-gradient(left, #ffefed 95%, #fbcfc9 100%);
  -webkit-box-shadow: inset 0 0 10px #fee4fc;
  -moz-box-shadow: inset 0 0 10px #fee4fc;
  -o-box-shadow: inset 0 0 10px #fee4fc;
  -ms-box-shadow: inset 0 0 10px #fee4fc;
  box-shadow: inset 0 0 10px #fee4fc;
}
</style>
