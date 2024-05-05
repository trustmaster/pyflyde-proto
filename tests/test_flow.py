import logging
import unittest
from flyde.io import EOF
from flyde.flow import Flow

logging.basicConfig(level=logging.DEBUG)


class TestIsolatedFlow(unittest.TestCase):
    def test_flow(self):
        flow = Flow.from_file("tests/TestIsolatedFlow.flyde")
        flow.run()
        flow.stopped.wait()
        self.assertTrue(flow.stopped.is_set())


class TestInOutFlow(unittest.TestCase):
    def test_flow(self):
        test_case = {
            "inputs": ["Hello", "World", EOF],
            "outputs": ["Hello", "World", EOF],
        }
        flow = Flow.from_file("tests/TestInOutFlow.flyde")

        in_q = flow.node.inputs["inMsg"].queue
        out_q = flow.node.outputs["outMsg"].queue

        flow.run()

        for inp, out in zip(test_case["inputs"], test_case["outputs"]):
            in_q.put(inp)
            self.assertEqual(out, out_q.get())

        flow.stopped.wait()
        self.assertTrue(flow.stopped.is_set())


# class TestNestedFlow(unittest.TestCase):
#     def test_flow(self):
#         test_case = {
#             "inputs": {
#                 "inp": ["Hello", "World", "!", EOF],
#                 "n": [1, 2, EOF],
#             },
#             "outputs": [
#                 "HelloHelloHello",
#                 "WorldWorldWorldWorldWorldWorld",
#                 "!!!!!!",
#                 EOF,
#             ],
#         }
#         flow = Flow.from_file("tests/TestNestedFlow.flyde")

#         inp_q = flow.node.inputs["inp"].queue
#         n_q = flow.node.inputs["n"].queue
#         out_q = flow.node.outputs["out"].queue

#         flow.run()

#         for i, inp in enumerate(test_case["inputs"]["inp"]):
#             print(i, inp, test_case["outputs"][i])
#             inp_q.put(inp)
#             print("Sent inp")
#             if i < len(test_case["inputs"]["n"]):
#                 n_q.put(test_case["inputs"]["n"][i])
#                 print("Sent n")
#             out = out_q.get()
#             print("Asserting", test_case["outputs"][i], out)
#             self.assertEqual(test_case["outputs"][i], out)

#         flow.stopped.wait()
#         self.assertTrue(flow.stopped.is_set())
