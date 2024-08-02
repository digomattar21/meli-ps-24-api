from heart.structures.verify import verifyJson


# def verify(next):
#     def decorator(self, **data):
#         body = self.getJsonBody()
#         errors = verifyJson(
#             json=body,
#             requiredParameters=["spotId"]
#         )
#         if errors:
#             return self.sendJson({"errors": errors})

#         data.update({
#             "spotId": body["spotId"]
#         })
#         return next(self, **data)
#     return decorator

def verifyTicketGet(next):
    def decorator(self, **data):
        id = self.getParameter("id", None)
        
        data.update({
            "id": id,
        })
        return next(self, **data)
    return decorator
