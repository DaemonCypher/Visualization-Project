import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			fallback: '404.html',
		}),
		paths: {
			// base: process.argv.includes('dev') ? '' : '/Visualization-Project'
			base: '/Visualization-Project',
		},
	},
};

export default config;