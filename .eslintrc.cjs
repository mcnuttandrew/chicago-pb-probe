module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: ["standard"],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: ["@typescript-eslint"],
  rules: {
    quotes: 0,
    "comma-dangle": 0,
    semi: 0,
    "space-before-function-paren": 0,
  },
};
