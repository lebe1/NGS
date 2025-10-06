/**
 * Create a route matching a specific method and pathname.
 * Both method and pathname have to match for a route to be taken.
 * @class
 */
export class Route {
	/**
	 * Route constructor. 
	 * @param {string} method - the method to use.
	 * @param {string} pathname - the pathname of the route.
	 * @param {Function} callback - the callback function to invoke when the route matches.
	 * @constructor
	 */
	constructor(method, pathname, callback) {
	}

	/**
	 * Check whether the route matches.
	 * A route to match have to have the same pathname and method.
	 * @param {string} method - the method to use.
	 * @param {string} pathname - the pathname of the route.
	 * @return {boolean} whether the route matches or not.
	 */
	match(method, pathname) {
		// to complete
	}
}

export default Route;
