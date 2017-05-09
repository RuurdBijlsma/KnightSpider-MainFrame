from ik import Arm

arm = Arm(['z', [80, 0., 0.], 'y', [80, 0., 0.], 'y', [40, 0., 0.]])
angles = arm.inverseKinematics(-180, 50, -60)
print("Angles", angles)
print("Position", arm.forwardKinematics(angles))
