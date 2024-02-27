import { asynchandler } from "../utils/asynchandler.js";
import {ApiUrl} from "../models/ApiUrl.model.js";
import { apiError } from "../utils/ApiError.js";

/**
 * Registers a new product.
 * 
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Object} - The response object with a success message.
 * @throws {apiError} - If the product ID or URL already exists, or if the required fields are missing.
 */
const registerProduct = asynchandler(async (req, res) => {
        const body = req.body;
        console.log(body);
        const newProduct = {
                site: body.Product_site,
                prod_id: body.Product_ID,
                url: body.Product_URL,
        };
        const prodExists = await ApiUrl.findOne({
                $or: [{prod_id: newProduct.prod_id}, {url: newProduct.url}]
        })
        if (prodExists) {
                throw new apiError(409, 'Product ID or URL already exists');
        }
        if (!newProduct.prod_id || !newProduct.url || !newProduct.site) {
                throw new apiError(404, 'Product ID, URL or site are missing');
        }
        
        await ApiUrl.create(newProduct);
        res.json({message: "product registered"});
        console.log("product registered in the DB")
});

/**
 * Retrieves all products from the database.
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {void}
 */
const getAllProducts = asynchandler(async (req, res) => {
        const allproducts = await ApiUrl.find();
        res.json(allproducts);
        console.log("getAllProducts called successfully")
});

/**
 * Get product by ID.
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Promise<void>} - A promise that resolves with the product data.
 * @throws {apiError} - If the query parameter 'prod_id' is missing or if the product is not found.
 */
const getProductById = asynchandler(async (req, res) => {
        let queryparam = req.query.prod_id;
        if(!queryparam)
        {
                throw new apiError(404, 'query param prod_id missing');
        }
        console.log(queryparam);
        const product = await ApiUrl.findOne({prod_id: queryparam});
        if (!product) {
                throw new apiError(404, 'Product not found');
        }
        res.json(product);
        console.log("getProductById called successfully")
});

/**
 * Deletes a product by its ID.
 *
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Promise<void>} - A promise that resolves when the product is deleted successfully.
 * @throws {apiError} - If the query parameter 'prod_id' is missing or the product is not found.
 */
const deleteProductById = asynchandler(async (req, res) => {
        let queryparam = req.query.prod_id;
        if(!queryparam)
        {
                throw new apiError(404, 'query param prod_id missing');
        }
        console.log(queryparam);
        const product = await ApiUrl.findOneAndDelete({prod_id: queryparam});
        if (!product) {
                throw new apiError(404, 'Product not found');
        }
        res.json({message: 'Product deleted successfully'});
        console.log("deleteProductById called successfully")
});

const deleteAllProducts = asynchandler(async (req, res) => {
        await ApiUrl.deleteMany({});
        res.json({message: 'All products deleted successfully'});
        console.log("deleteAllProducts called successfully")
});

export { registerProduct, getAllProducts, getProductById, deleteProductById, deleteAllProducts }
// This is the default export for this module
