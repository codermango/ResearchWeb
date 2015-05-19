def validation(R,T):
	hit=0
	for r in R:
		if r in T:
			hit=hit+1
	precision=float(hit)/float(len(R))
	recall=float(hit)/float(len(T))
	print hit
	print precision
	print recall
	print precision/recall
	return R+T

# infile=open('myfavorite.txt','r')
# num=0
# l1=[]
# l2=[]
# for line in infile:
# 	num=num+1
# 	iid= line.replace('\n','')
# 	if num<20:
# 		l1.append(iid)
# 	if num>10:
# 		l2.append(iid)

# print validation (l1,l2)



t = ["tt0343818","tt0480249","tt0482571","tt1130884","tt0289879","tt0309698","tt0209144","tt0361862","tt0338564","tt0068646","tt0111161","tt0105859","tt077082"]
r = [u'tt0107302', u'tt0066565', u'tt0338564', u'tt0100797', u'tt0061811', u'tt0421715', u'tt0449467', u'tt0071315', u'tt0114746', u'tt0118972', u'tt0478304', u'tt0119488', u'tt0332452', u'tt0119643', u'tt0056757', u'tt0364569', u'tt1001526', u'tt1839578', u'tt1358522', u'tt0129686', u'tt0035317', u'tt0073138', u'tt1255953', u'tt0069293', u'tt0044954', u'tt0075029', u'tt0088146', u'tt0120102', u'tt0063442', u'tt0083100', u'tt0369258', u'tt0096639', u'tt0409459', u'tt1210166', u'tt0093640', u'tt0047878', u'tt0046912', u'tt0043961', u'tt0041268', u'tt0036323', u'tt2713180', u'tt0117665', u'tt0052902', u'tt0498380', u'tt0061578', u'tt0049233', u'tt1788634', u'tt0114369', u'tt0059856', u'tt0349903', u'tt0113617', u'tt1699748', u'tt0110322', u'tt0051083', u'tt0071042', u'tt0039017', u'tt0052561', u'tt0104348', u'tt0054102', u'tt0421238', u'tt0034820', u'tt0033786', u'tt0059418', u'tt0356910', u'tt0773262', u'tt0266987', u'tt0118401', u'tt0032484', u'tt0040897', u'tt0062622', u'tt1235099', u'tt0062626', u'tt0327056', u'tt0017925', u'tt0137523', u'tt0416449', u'tt0496806', u'tt0105435', u'tt0110148', u'tt0083944', u'tt0025607', u'tt0419294', u'tt0477507', u'tt0887883', u'tt0060196', u'tt1515091', u'tt0988045', u'tt0120768', u'tt0105585', u'tt0443680', u'tt1375666', u'tt0013086', u'tt0062038', u'tt0105265', u'tt0078655', u'tt0062138', u'tt0208092', u'tt0240772', u'tt0236493', u'tt0047849']
# tt0773262
print set(t).intersection(set(r))
print len(t), len(r)

validation(r, t)