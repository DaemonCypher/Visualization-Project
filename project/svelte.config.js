import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			fallback: '404.html'
		}),
		paths: {
			// TODO: base path might be wrong here
			base: process.argv.includes('dev') ? '' : '/Visualization-Project/'
		}
	}
};

export default config;