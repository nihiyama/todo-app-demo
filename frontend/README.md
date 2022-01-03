# frontend

## setup

1. setup development with devcontainer. (see .devcontainer dir)
    - choose node.js container.
    - preinstall vue/cli.

2. vue create project
    - vue create \<project name>
        ```
        # summary
        ? Please pick a preset: Manually select features
        ? Check the features needed for your project: Choose Vue version, Babel, TS, Router, Vuex, Linter, Unit, E2E
        ? Choose a version of Vue.js that you want to start the project with 2.x
        ? Use class-style component syntax? No
        ? Use Babel alongside TypeScript (required for modern mode, auto-detected polyfills, transpiling JSX)? No
        ? Use history mode for router? (Requires proper server setup for index fallback in production) Yes
        ? Pick a linter / formatter config: Standard
        ? Pick additional lint features: Lint on save
        ? Pick a unit testing solution: Jest
        ? Pick an E2E testing solution: Cypress
        ? Where do you prefer placing config for Babel, ESLint, etc.? In package.json
        ? Save this as a preset for future projects? No


        # setup questions
        ? Please pick a preset: 
        Default ([Vue 2] babel, eslint) 
        Default (Vue 3) ([Vue 3] babel, eslint) 
        ❯ Manually select features

        ? Check the features needed for your project: 
         ◉ Choose Vue version
         ◉ Babel
         ◉ TypeScript
         ◯ Progressive Web App (PWA) Support
         ◉ Router
         ◉ Vuex
         ◯ CSS Pre-processors
         ◉ Linter / Formatter
         ◉ Unit Testing
        ❯◉ E2E Testing

        ? Choose a version of Vue.js that you want to start the project with (Use arrow keys)
        ❯ 2.x 
          3.x
        
        ? Use class-style component syntax? (Y/n) n

        ? Use Babel alongside TypeScript (required for modern mode, auto-detected polyfills, transpiling JSX)? (Y/n) n

        ? Use history mode for router? (Requires proper server setup for index fallback in production) (Y/n) Y

        ? Pick a linter / formatter config: 
          ESLint with error prevention only 
          ESLint + Airbnb config 
        ❯ ESLint + Standard config 
          ESLint + Prettier 
          TSLint (deprecated)
        
        ? Pick additional lint features: (Press <space> to select, <a> to toggle all, <i> to invert selection)
        ❯◉ Lint on save
         ◯ Lint and fix on commit
        
        ? Pick a unit testing solution: 
          Mocha + Chai 
        ❯ Jest

        ? Pick an E2E testing solution: 
        ❯ Cypress (Chrome only) 
          Nightwatch (WebDriver-based) 
          WebdriverIO (WebDriver/DevTools based)

        ? Where do you prefer placing config for Babel, ESLint, etc.?
          In dedicated config files 
        ❯ In package.json

        ? Save this as a preset for future projects? (y/N) N
        ```
    
    - vue add vuetify
        ```
        ? Choose a preset: (Use arrow keys)
          Configure (advanced) 
        ❯ Default (recommended) 
          Vite Preview (Vuetify 3 + Vite) 
          Prototype (rapid development) 
          Vuetify 3 Preview (Vuetify 3) 
        ```
    
    - npm install vuex-persistedstate secure-ls

    - npm install @vue/composition-api
  
