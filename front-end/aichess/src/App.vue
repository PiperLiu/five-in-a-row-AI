<template>
  <nav>
    <router-link to="/">AI Chess</router-link> |
    <a href="https://github.com/PiperLiu/five-in-a-row-AI">Fork Me On GitHub</a> |
    <a href="https://piperliu.xyz">About Me</a>
  </nav>
  <router-view/>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
