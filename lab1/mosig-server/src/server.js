import http from 'node:http';
import fs from 'node:fs';
import MIME_TYPES from './mime-types.js';
import Route from './route.js';

/**
 * Create an HTTP server listening to a specific port.
 * This class is mainly a wrapper around http.Server.
 * @see {http.Server}
 * @class
 */
export class Server {

	/**
	 * A collection of routes.
	 * @type {Array.<Route>}
	 * @default EMPTY_COLLECTION
	 */
	#routes = [];

	/**
	 * The HTTP server to launch.
	 * @type {http.Server}
	 */
	#server;

	/**
	 * Start the server on a specific user port.
	 * @param {number} port - a port number (between 1024–49151).
	 */
	start(port = 8080) {

		this.#server = http.createServer(function (req, res) {

			const { method } = req; // the method (GET, POST, etc.) from the client request

			const url = new URL(req.url, `http://${req.headers.host}`); // Destructuring the URL

			const { pathname } = url; // the pathname extracted from the URL

			console.log(pathname); // display the pathname for debugging purpose.

			const isAsset = false; // <-- to modify

			if (isAsset) {
				// Handle assets in a generic way
			}
			else {
				// Handle views according to routes.
				// Replace the code below.
				fs.readFile('./views/main.html', (err, data) => {
					if (err) {
						res.writeHead(404, { 'Content-Type': 'text/plain' });
						res.end('404 not found');
					}
					else {
						res.writeHead(200, { 'Content-Type': 'text/html' });
						res.end(data);
					}
				});
			}
		});
		console.log(`Server is started on port ${port}`);
		this.#server.listen(port);
	}
}

export default Server;
