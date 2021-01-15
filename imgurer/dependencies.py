from fastapi import Header

async def valid_content_length(content_length: int = Header(..., lt=12_000)):
    """
        Defines the maximum size of content allowed as sent by the header. Does not prevent client sending invalid header.
    """
    return content_length