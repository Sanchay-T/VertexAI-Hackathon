# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# def execute_code(code: str, allowed_modules: dict) -> dict:
#     # create a dictionary of allowed names
#     safe_dict = {name: allowed_modules[name] for name in allowed_modules if name in globals()}

#     # add '__builtins__' to the dictionary to allow built-in functions
#     safe_dict['__builtins__'] = __builtins__

#     # create a dictionary to hold the result of the execution
#     result_dict = {}

#     # execute the code in the context of the safe dictionary
#     exec(code, safe_dict, result_dict)

#     return result_dict

# code = """
# df = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
# df.plot.bar()
# plt.savefig('bar_plot.png')
# """

# allowed_modules = {'pd': pd, 'plt': plt, 'np': np}
# result = execute_code(code, allowed_modules)

from codeinterpreterapi import CodeInterpreterSession


async def main():
    # create a session
    session = CodeInterpreterSession()
    await session.astart()

    # generate a response based on user input
    response = await session.generate_response(
        "Plot the bitcoin chart of 2023 YTD"
    )

    # output the response (text + image)
    print("AI: ", response.content)
    for file in response.files:
        file.show_image()

    # terminate the session
    await session.astop()


if __name__ == "__main__":
    import asyncio
    # run the async function
    asyncio.run(main())
