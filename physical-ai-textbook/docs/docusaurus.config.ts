import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import * as dotenv from 'dotenv';

// Load environment variables from .env.development or .env.production
dotenv.config({ path: process.env.NODE_ENV === 'production' ? '.env.production' : '.env.development' });

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'From Digital Intelligence to Embodied Systems',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://hackathon-1-physical-ai-textbook-phi.vercel.app',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/',

  // GitHub pages deployment config.
  organizationName: 'MuhammadZarwali', // Usually your GitHub org/user name.
  projectName: 'hackathon-1-physical-ai-textbook-', // Usually your repo name.

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // Custom fields to expose environment variables to React components
  customFields: {
    API_URL: process.env.API_URL || 'http://localhost:8001',
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/', // Docs-only mode
          sidebarPath: './sidebars.ts',
          editUrl: undefined,
        },
        blog: false, // Disable blog
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Textbook',
        },
        {
          href: 'https://github.com/MuhammadZarwali/Hackathon',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Textbook',
          items: [
            {
              label: 'Introduction',
              to: '/',
            },
            {
              label: 'Module 1: ROS 2',
              to: '/module-1-ros2/chapter-1-introduction-to-ros2',
            },
            {
              label: 'Module 2: Simulation',
              to: '/module-2-simulation/chapter-1-introduction-to-digital-twins',
            },
            {
              label: 'Module 3: Isaac AI Brain',
              to: '/module-3-isaac-ai-brain/chapter-1-introduction-to-nvidia-isaac',
            },
            {
              label: 'Module 4: VLA Models',
              to: '/module-4-vision-language-action/chapter-1-introduction-to-vla',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'ROS 2 Documentation',
              href: 'https://docs.ros.org/en/humble/',
            },
            {
              label: 'Hackathon Project',
              href: 'https://github.com/MuhammadZarwali/Hackathon',
            },
          ],
        },
        {
          title: 'Connect',
          items: [
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/in/muhammad-zarwali-b3260a2b4',
            },
            {
              label: 'GitHub Profile',
              href: 'https://github.com/MuhammadZarwali',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Muhammad Zarwali - Physical AI Textbook Project. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
