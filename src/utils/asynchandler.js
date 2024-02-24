import { Promise } from "mongoose"

const asynchandler = (requesthandler) => {
    (req, res, next) => {
        Promise.resolve(requesthandler(req, res, next))
        .catch((error) => next(error));
    }
}

export { asynchandler }