##  ConcurrentHashMap��HashMapʹ�ñȽ�

#### HashMap�ڶ��̻߳����µ�����

1. ���̻߳����£�ʹ��Hashmap����put������������ѭ��������CPU�����ʽӽ�100%�������ڲ�������²���ʹ��HashMap����Ȼ�Ѿ���һ���̰߳�ȫ��HashTable������HashTable����ʹ��synchronized������get��put������ʵ�ִ������£�����֤�̰߳�ȫ�����߳̾������ҵ������HashTable��Ч�ʷǳ����¡���Ϊ��һ���̷߳���HashTable��ͬ������ʱ����������ͬ���������߳̾Ϳ��ܻ��������������ѵ״̬��
   ���߳�1ʹ��put�������Ԫ�أ��߳�2��������ʹ��put�������Ԫ�أ�����Ҳ����ʹ��get��������ȡԪ�أ����Ծ���Խ����Ч��Խ�͡�
2. ConcurrentHashMap����ͨ��hashmap��ɶ���𡣿������κγ��ϴ���HashMap��
   1. ���̰߳�ȫ�ģ���ͨ��hashmap����ȫ��hashtable���̰߳�ȫ��Synchronized��
   2. Ч��Ҫ��hashmap��Ч�����߳����ݵȣ�
   3. ��hashmapһ������size������ֵʱ�������ݲ��ҽṹ���ɺ����
   4. hashmap��key��value����������Ϊnull��ConcurrentHashMap��hashtable���ǲ����Ե�
   5. ��hashmapһ���ڲ��ṹʹ�������飬���������
   ���ۣ��ڶ��̵߳Ļ����£�Ӧ������ѡ���̰߳�ȫ�Ҹ�Ч��ConcurrentHashMap��
