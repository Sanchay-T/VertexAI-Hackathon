from codeinterpreterapi import CodeInterpreterSession, File


async def main():
    # context manager for auto start/stop of the session
    async with CodeInterpreterSession() as session:
        # define the user request
        user_request = "Analyze this dataset and plot something interesting about it."
        files = [
            File.from_path("HRDataset_v14.csv"),
        ]

        # generate the response
        response = await session.generate_response(
            user_request, files=files
        )

        # output to the user
        print("AI: ", response.content)
        for file in response.files:
            file.show_image()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())