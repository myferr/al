import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Al",
  description: "A conversational Discord.py AI chat-bot",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: "Home", link: "/" },
      { text: "Introduction", link: "/introduction" },
    ],

    sidebar: [
      {
        text: "Introduction",
        items: [
          { text: "Introduction", link: "/introduction" },
          { text: "Interaction", link: "/Interaction" },
          { text: "Features", link: "/features" },
        ],
      },
      {
        text: "Self Hosting",
        items: [
          { text: "Prerequisites", link: "/prerequisites" },
          { text: "Installation", link: "/installation" },
          { text: "Customization", link: "/customization" },
          { text: "Memory", link: "/memory" },
          { text: "Troubleshooting", link: "/troubleshooting" },
        ],
      },
      {
        text: "Miscellaneous",
        items: [
          { text: "Terms of Service", link: "/terms" },
          { text: "Privacy Policy", link: "/privacy" },
        ],
      },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/myferr/al" },
      {
        icon: "discord",
        link: "https://discord.com/oauth2/authorize?client_id=1394016191537741957",
      },
    ],
  },
});
