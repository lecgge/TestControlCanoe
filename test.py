import sys
from time import sleep
import win32com.client

CANoe = win32com.client.Dispatch('CANoe.Application')
CANoe.Open("D:\\GalaxyTest\\GalaxyTest\\Configuration.cfg")

test_env = CANoe.Configuration.TestSetup.TestEnvironments.Item("HardTest")

# Cast required since test_env is originally of type <ITestEnvironment>
test_env = win32com.client.CastTo(test_env, "ITestEnvironment2")
# Get the XML TestModule (type <TSTestModule>) in the test setup
test_module = test_env.TestModules.Item('HardTest')
# {.Sequence} property returns a collection of <TestCases> or <TestGroup>
# or <TestSequenceItem> which is more generic
seq = test_module.Sequence
# a = seq.Item(1).Sequence.Count
for i in range(1, seq.Count+1):
    # Cast from <ITestSequenceItem> to <ITestCase> to access {.Verdict}
    # and the {.Enabled} property
    tc = win32com.client.CastTo(seq.Item(i), "ITestCase")
    print(tc.Name)
    tc.Enabled = True
    # if tc.Verdict != 1: # Verdict 1 is pass
    #     tc.Enabled = True
    #     print(f"Enabling Test Case {tc.Ident} with verdict {tc.Verdict}")
    # else:
    #     tc.Enabled = False
    #     print(f"Disabling Test Case {tc.Ident} since it has already passed")


# CANoe.Measurement.Start()
# sleep(5)   # Sleep because measurement start is not instantaneous
# test_module.Start()
# sleep(1)