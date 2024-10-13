from fastapi import Depends, HTTPException, Request, status


def validate_query_params(expected_params: set):
    """
    Зависимость, которая используется для установления конечных параметров в самом endpoint,
    чтобы нельзя было внедрить любые другие возможные параметры, и, как иную возможность - SQL инъекцию.

    """

    async def dependency(request: Request):
        actual_params = set(request.query_params.keys())
        unexpected_params = actual_params - expected_params
        if unexpected_params:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unexpected query parameters: {', '.join(unexpected_params)}",
            )

    return Depends(dependency)
